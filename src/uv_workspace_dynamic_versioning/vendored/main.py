from __future__ import annotations

import os
import re
from functools import partial
from pathlib import Path

import tomlkit
from dunamai import _VALID_PEP440, _VALID_PVP, _VALID_SEMVER, Style, Version

from .template import render_template

from . import schemas


def read(root: str):
    pyproject = Path(root) / "pyproject.toml"
    return pyproject.read_text()


def parse(text: str):
    return tomlkit.parse(text)


def validate(project: tomlkit.TOMLDocument):
    return schemas.Project.from_dict(project.unwrap())


def _get_bypassed_version() -> str | None:
    return os.environ.get("UV_DYNAMIC_VERSIONING_BYPASS")


def check_version_style(version: str, style: Style = Style.Pep440) -> None:
    """Check if a version is valid for a style."""
    name, pattern = {
        Style.Pep440: ("PEP 440", _VALID_PEP440),
        Style.SemVer: ("Semantic Versioning", _VALID_SEMVER),
        Style.Pvp: ("PVP", _VALID_PVP),
    }[style]
    failure_message = f"Version '{version}' does not conform to the {name} style"
    if not re.search(pattern, version):
        raise ValueError(failure_message)

    if style == Style.SemVer:
        parts = re.split(r"[.-]", version.split("+", 1)[0])
        if any(re.search(r"^0[0-9]+$", x) for x in parts):
            raise ValueError(failure_message)


def _get_from_file_version(config: schemas.UvWorkspaceDynamicVersioning) -> str | None:
    if config.from_file is None:
        return None

    source, pattern = (config.from_file.source, config.from_file.pattern)
    content = Path(source).read_text().strip()

    if pattern is None:
        return content

    result = re.search(pattern, content, re.MULTILINE)
    if result is None:
        raise ValueError(f"File '{source}' did not contain a match for '{pattern}'")
    return str(result.group(1))


import subprocess
def patch_version_for_directory(version: Version, path: Path) -> Version:
    """
    Patches a Dunamai Version object to reflect the history of a specific subdirectory.

    In a monorepo/workspace, the root git distance and commit hash might not
    reflect changes to a specific package. This function re-calculates the
    distance and latest commit by filtering git history to the provided path.

    Args:
        version (Version): The original version object from Dunamai.
        path (Path): The directory path to filter history by.

    Returns:
        Version: The updated version object with directory-specific metadata.
    """
    matched_tag = getattr(version, "_matched_tag", None)

    try:
        if matched_tag:
            rev_list_cmd = ["git", "rev-list", f"{matched_tag}..HEAD", "--", str(path)]
            out = subprocess.check_output(rev_list_cmd, cwd=path, text=True, stderr=subprocess.DEVNULL).strip()
            distance = len(out.splitlines()) if out else 0

            log_cmd = ["git", "log", "-1", "--format=%H", f"{matched_tag}..HEAD", "--", str(path)]
            commit_out = subprocess.check_output(log_cmd, cwd=path, text=True, stderr=subprocess.DEVNULL).strip()
        else:
            rev_list_cmd = ["git", "rev-list", "HEAD", "--", str(path)]
            out = subprocess.check_output(rev_list_cmd, cwd=path, text=True, stderr=subprocess.DEVNULL).strip()
            distance = len(out.splitlines()) if out else 0

            log_cmd = ["git", "log", "-1", "--format=%H", "HEAD", "--", str(path)]
            commit_out = subprocess.check_output(log_cmd, cwd=path, text=True, stderr=subprocess.DEVNULL).strip()

        if commit_out:
            commit_length = len(version.commit) if version.commit else 7
            version.commit = commit_out[:commit_length]
            version.distance = distance
        else:
            version.distance = 0

        status_cmd = ["git", "status", "--porcelain", "--", str(path)]
        status_out = subprocess.check_output(status_cmd, cwd=path, text=True, stderr=subprocess.DEVNULL).strip()
        version.dirty = bool(status_out)
    except Exception:
        pass

    return version

def _get_version(config: schemas.UvWorkspaceDynamicVersioning, project_dir: Path) -> Version:
    try:
        return Version.from_vcs(
            config.vcs,
            path=project_dir,
            latest_tag=config.latest_tag,
            strict=config.strict,
            tag_branch=config.tag_branch,
            tag_dir=config.tag_dir,
            full_commit=config.full_commit,
            ignore_untracked=config.ignore_untracked,
            pattern=config.pattern,
            pattern_prefix=config.pattern_prefix,
            commit_length=config.commit_length,
        )
    except RuntimeError as e:
        if fallback_version := config.fallback_version:
            return Version(fallback_version)
        raise e


def get_version(config: schemas.UvWorkspaceDynamicVersioning, project_dir: Path) -> tuple[str, Version]:
    """
    Calculates and serializes the project version.

    This is the core logic for version retrieval. It handles:
    1. Environment variable bypass (`UV_DYNAMIC_VERSIONING_BYPASS`).
    2. Version retrieval from a file (`from-file` config).
    3. VCS-based version detection via Dunamai.
    4. Directory-specific history patching.
    5. Version bumping and formatting (Jinja2 or Dunamai style).

    Args:
        config (UvWorkspaceDynamicVersioning): The plugin configuration.
        project_dir (Path): The root directory of the project.

    Returns:
        tuple[str, Version]: A tuple of (serialized_version_string, Version_object).
    """
    bypassed = _get_bypassed_version()
    if bypassed:
        parsed = Version.parse(bypassed, pattern=config.pattern)
        return bypassed, parsed

    from_file = _get_from_file_version(config)
    if from_file:
        parsed = Version.parse(from_file, pattern=config.pattern)
        return from_file, parsed

    got = _get_version(config, project_dir)
    got = patch_version_for_directory(got, project_dir)
    
    effective_dirty = config.dirty if config.dirty is not None else got.dirty

    if config.format_jinja:
        updated = (
            got.bump(index=config.bump_config.index)
            if config.bump_config.enable and got.distance > 0
            else got
        )
        serialized = render_template(
            config.format_jinja, version=updated, config=config
        )
        if config.style:
            check_version_style(serialized, config.style)
    else:
        updated = (
            got.bump(smart=True, index=config.bump_config.index)
            if config.bump_config.enable
            else got
        )
        serialized = updated.serialize(
            metadata=config.metadata,
            style=config.style,
            dirty=effective_dirty,
            tagged_metadata=config.tagged_metadata,
            format=config.format,
            escape_with=config.escape_with,
            commit_prefix=config.commit_prefix,
        )

    return (serialized, updated)
