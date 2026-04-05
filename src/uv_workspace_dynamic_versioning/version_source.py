"""Dynamic workspace version source for hatch.

This module provides the DynamicWorkspaceVersionSource class that implements
hatch's VersionSourceInterface to enable dynamic version detection from
VCS (git) with workspace-aware directory-specific history patching.
"""

from __future__ import annotations

import os
import re
import subprocess  # nosec B404
import sys
from functools import cached_property
from pathlib import Path

import tomlkit
from dunamai import Style, Version
from hatchling.version.source.plugin.interface import VersionSourceInterface

from .schemas import PluginConfig, load_project_config
from .template import render_jinja_template

# Standard version patterns (adapted from dunamai)
_VALID_PEP440 = r"^(?:\d+!)?\d+(?:\.\d+)*((?:a|b|rc)\d+)?(?:\.post\d+)?(?:\.dev\d+)?(?:\+[a-zA-Z0-9](?:[a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9.]*[a-zA-Z0-9])?)?$"
_VALID_SEMVER = r"^\d+\.\d+\.\d+(?:-[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*)?(?:\+[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*)?$"
_VALID_PVP = r"^\d+(?:\.\d+)*(?:-[a-zA-Z0-9]+)*$"


def check_version_style(version: str, style: Style = Style.Pep440) -> None:
    """Validate that a version string conforms to the specified style.

    Args:
        version: The version string to validate
        style: The style to validate against (PEP 440, SemVer, or PVP)

    Raises:
        ValueError: If the version doesn't conform to the style
    """
    pattern = {
        Style.Pep440: _VALID_PEP440,
        Style.SemVer: _VALID_SEMVER,
        Style.Pvp: _VALID_PVP,
    }.get(style, _VALID_PEP440)

    if not re.search(pattern, version):
        raise ValueError(f"Version '{version}' does not conform to {style.name} style")


def _get_bypass_version(project_dir: Path) -> str | None:
    """Check for version bypass environment variables.
    
    Supports both global bypass and package-specific overrides via:
    - UV_WORKSPACE_DYNAMIC_VERSIONING_OVERRIDE (e.g. "pkg1=1.0.0, pkg2=2.0.0")
    - UV_WORKSPACE_DYNAMIC_VERSIONING_BYPASS (global fallback)
    - UV_DYNAMIC_VERSIONING_BYPASS (legacy global fallback)
    """
    # 1. Check for package-specific overrides
    override_str = os.environ.get("UV_WORKSPACE_DYNAMIC_VERSIONING_OVERRIDE") or os.environ.get("UV_DYNAMIC_VERSIONING_OVERRIDE")
    if override_str:
        try:
            pyproject_path = project_dir / "pyproject.toml"
            if pyproject_path.is_file():
                content = pyproject_path.read_text(encoding="utf-8")
                import tomlkit
                data = tomlkit.parse(content)
                project_name = data.get("project", {}).get("name")
                
                if project_name:
                    for part in override_str.split(","):
                        if "=" in part:
                            k, v = part.split("=", 1)
                            if k.strip() == project_name:
                                return v.strip()
        except Exception:
            pass

    # 2. Check for global bypass
    bypass = os.environ.get("UV_WORKSPACE_DYNAMIC_VERSIONING_BYPASS")
    if bypass:
        return bypass

    # 3. Legacy bypass
    return os.environ.get("UV_DYNAMIC_VERSIONING_BYPASS")


def _get_workspace_version(project_dir: Path) -> str | None:
    """Find a static project version in any parent pyproject.toml.

    Args:
        project_dir: The project directory

    Returns:
        The version string if found, None otherwise
    """
    current = project_dir.resolve()
    for dir_path in [current, *current.parents]:
        pyproject_path = dir_path / "pyproject.toml"
        if not pyproject_path.is_file():
            continue

        try:
            content = pyproject_path.read_text(encoding="utf-8")
            data = tomlkit.parse(content)
            
            project = data.get("project", {})
            if isinstance(project, dict):
                version = project.get("version")
                if version and isinstance(version, str):
                    return version
        except Exception:
            pass

    return None


class DynamicWorkspaceVersionSource(VersionSourceInterface):
    """Dynamic version source that reads version from VCS (git) with workspace support.

    This plugin extends hatch's version source system to provide:
    - VCS-based version detection using dunamai
    - Directory-specific git history patching for workspaces
    - Jinja2 template rendering for version strings
    - Multiple version format styles (PEP 440, SemVer, PVP)
    - Environment variable bypass for CI/CD pipelines
    """

    PLUGIN_NAME = "uv-workspace-dynamic-versioning"

    @cached_property
    def config(self) -> PluginConfig:
        """Load and cache the plugin configuration."""
        return load_project_config(self.root)

    def get_version_data(self) -> dict[str, str]:
        """Retrieve the version for the project.

        This is the main entry point called by hatch to get the version string.
        It handles:
        1. Environment variable bypass
        2. File-based version reading
        3. VCS-based version detection
        4. Directory-specific history patching
        5. Jinja2 template formatting

        Returns:
            Dictionary containing the 'version' key with the version string
        """
        version_str, _ = get_version(self.config, Path(self.root))
        return {"version": version_str}


def _read_version_from_file(config: PluginConfig, project_dir: Path) -> str | None:
    """Read version from a file based on configuration.

    Args:
        config: The plugin configuration
        project_dir: The project directory

    Returns:
        The version string if read from file, None otherwise
    """
    from_file = config.get_from_file()
    if from_file is None:
        return None

    source_path = (project_dir / from_file.source).resolve()

    # Security: Ensure the file is within the project directory
    try:
        source_path.relative_to(project_dir.resolve())
    except ValueError as e:
        raise ValueError(f"File '{from_file.source}' is outside of the project root") from e

    if not source_path.is_file():
        raise FileNotFoundError(f"Version file '{from_file.source}' does not exist")

    content = source_path.read_text().strip()

    if from_file.pattern is None:
        return content

    match = re.search(from_file.pattern, content, re.MULTILINE)
    if match is None:
        raise ValueError(f"Pattern '{from_file.pattern}' did not match in '{from_file.source}'")
    return str(match.group(1))


def _get_vcs_version(config: PluginConfig, project_dir: Path, ws_version: str | None = None) -> Version:
    """Get version from VCS (git) using dunamai.

    Args:
        config: The plugin configuration
        project_dir: The project directory
        ws_version: Optional workspace fallback version

    Returns:
        The Version object from dunamai
    """
    try:
        v = Version.from_vcs(
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
        if v.base == "0.0.0" and not config.fallback_version and not ws_version:
            print(
                f"uv-workspace-dynamic-versioning: No tags found matching pattern '{config.pattern}'. "
                "Returning 0.0.0. Use [tool.uv-workspace-dynamic-versioning] pattern to configure.",
                file=sys.stderr,
            )
        return v
    except RuntimeError as e:
        if ws_version:
            parsed = Version.parse(ws_version)
            parsed.distance = 0
            parsed.commit = ""
            parsed.dirty = False
            return parsed
        if config.fallback_version:
            return Version(config.fallback_version)
        print(
            f"uv-workspace-dynamic-versioning: VCS version detection failed: {e}",
            file=sys.stderr,
        )
        raise e


def _patch_version_for_directory(version: Version, path: Path) -> Version:
    """Patch version metadata for directory-specific git history.

    In a monorepo/workspace, the root git distance and commit hash might not
    reflect changes to a specific package. This re-calculates the distance
    and latest commit by filtering git history to the provided path.

    Args:
        version: The original version from dunamai
        path: The directory path to filter history by

    Returns:
        Updated Version with directory-specific metadata
    """
    matched_tag = getattr(version, "_matched_tag", None)

    try:
        # Use "." as the path filter because we run the command from the package directory
        if matched_tag:
            rev_cmd = ["git", "rev-list", f"{matched_tag}..HEAD", "--", "."]
            log_cmd = ["git", "log", "-1", "--format=%H", f"{matched_tag}..HEAD", "--", "."]
        else:
            rev_cmd = ["git", "rev-list", "HEAD", "--", "."]
            log_cmd = ["git", "log", "-1", "--format=%H", "HEAD", "--", "."]

        # Get commit distance for this directory
        rev_out = subprocess.check_output(  # nosec B603
            rev_cmd, cwd=path, text=True, stderr=subprocess.DEVNULL
        ).strip()
        distance = len(rev_out.splitlines()) if rev_out else 0

        # Get latest commit for this directory
        commit_out = subprocess.check_output(  # nosec B603
            log_cmd, cwd=path, text=True, stderr=subprocess.DEVNULL
        ).strip()

        if commit_out:
            commit_len = len(version.commit) if version.commit else 7
            version.commit = commit_out[:commit_len]
            version.distance = distance
        else:
            # If no commits in this directory since the tag, distance is 0
            version.distance = 0

        # Check if directory is dirty
        status_cmd = ["git", "status", "--porcelain", "--", "."]
        status_out = subprocess.check_output(  # nosec B603
            status_cmd, cwd=path, text=True, stderr=subprocess.DEVNULL
        ).strip()
        version.dirty = bool(status_out)

    except Exception as e:
        print(
            f"uv-workspace-dynamic-versioning: directory patching failed: {e}",
            file=sys.stderr,
        )

    return version


def get_version(config: PluginConfig, project_dir: Path) -> tuple[str, Version]:
    """Calculate and serialize the project version.

    This is the core version calculation logic that handles:
    1. Environment variable bypass
    2. File-based version reading
    3. VCS-based version detection
    4. Directory-specific history patching
    5. Version bumping and formatting

    Args:
        config: The validated plugin configuration
        project_dir: The project root directory

    Returns:
        Tuple of (serialized_version_string, Version_object)
    """
    # 1. Check for environment variable bypass
    if bypassed := _get_bypass_version(project_dir):
        parsed = Version.parse(bypassed, pattern=config.pattern)
        return bypassed, parsed

    # 2. Check for file-based version
    if from_file := _read_version_from_file(config, project_dir):
        parsed = Version.parse(from_file, pattern=config.pattern)
        return from_file, parsed

    # 3. Check for workspace root version
    ws_version = _get_workspace_version(project_dir)

    # 4. Get version from VCS
    version = _get_vcs_version(config, project_dir, ws_version)

    # 5. Apply directory-specific patching for workspaces
    version = _patch_version_for_directory(version, project_dir)

    # 6. Override base version if workspace version is specified
    if ws_version:
        parsed_ws = Version.parse(ws_version)
        version.base = parsed_ws.base
        version.stage = parsed_ws.stage
        version.revision = parsed_ws.revision

    # 7. Determine effective dirty state
    effective_dirty = config.dirty if config.dirty is not None else version.dirty

    # 8. Apply bumping if configured
    bump_cfg = config.bump_config
    if bump_cfg.enable and version.distance > 0:
        version = version.bump(index=bump_cfg.index)

    # 9. Format and serialize
    if config.format_jinja:
        serialized = render_jinja_template(
            config.format_jinja,
            version=version,
            config=config,
        )
        if config.style:
            check_version_style(serialized, config.style)
    else:
        serialized = version.serialize(
            metadata=config.metadata,
            style=config.style,
            dirty=effective_dirty,
            tagged_metadata=config.tagged_metadata,
            format=config.format,
            escape_with=config.escape_with,
            commit_prefix=config.commit_prefix,
        )

    return serialized, version
