"""Jinja2 template rendering for version strings and dependencies.

This module provides a sandboxed Jinja2 environment for safely rendering
templates with version information and custom imports.
"""

from __future__ import annotations

import re
from datetime import datetime
from importlib import import_module

import jinja2.sandbox
from dunamai import Version, bump_version, serialize_pep440, serialize_pvp, serialize_semver

from .schemas import PluginConfig


# Sandboxed Jinja2 environment for security
_JINJA_ENV = jinja2.sandbox.SandboxedEnvironment()


def _base_part(base: str, index: int) -> int:
    """Get a specific part of a version base string.

    Args:
        base: The version base string (e.g., "1.2.3")
        index: The index of the part to retrieve (0=major, 1=minor, 2=patch)

    Returns:
        The integer value at the specified index, or 0 if not present
    """
    try:
        return int(base.split(".")[index])
    except (IndexError, ValueError):
        return 0


def _escape_branch(value: str | None, escape_with: str | None) -> str | None:
    """Escape branch names for use in version strings.

    Args:
        value: The branch name to escape
        escape_with: The character to use for escaping

    Returns:
        Escaped branch name, or None if input was None
    """
    if value is None:
        return None
    return re.sub(r"[^a-zA-Z0-9]", escape_with or "", value)


def _format_timestamp(value: datetime | None) -> str | None:
    """Format a datetime for use in version strings.

    Args:
        value: The datetime to format

    Returns:
        Formatted timestamp string (YYYYMMDDHHMMSS), or None if input was None
    """
    if value is None:
        return None
    return value.strftime("%Y%m%d%H%M%S")


def render_jinja_template(
    template_str: str,
    *,
    version: Version,
    config: PluginConfig,
) -> str:
    """Render a Jinja2 template with version context.

    This function provides a sandboxed Jinja2 environment with version
    metadata and helper functions available in the template context.

    Available template variables:
        - version: The dunamai Version object
        - base: The base version string (e.g., "1.2.3")
        - stage: The version stage (a, b, rc, etc.)
        - revision: The version revision number
        - distance: Number of commits since last tag
        - commit: The commit hash (truncated)
        - dirty: Whether the working directory has uncommitted changes
        - branch: The current branch name
        - tagged_metadata: Any metadata from the tag
        - major, minor, patch: Parts of the base version
        - timestamp: Formatted timestamp
        - branch_escaped: Escaped branch name

    Available template functions:
        - bump_version: Function to bump version parts
        - serialize_pep440: PEP 440 serializer
        - serialize_semver: SemVer serializer
        - serialize_pvp: PVP serializer

    Args:
        template_str: The Jinja2 template string to render
        version: The Version object to use in the template
        config: The plugin configuration (for escape_with setting)

    Returns:
        The rendered template string

    Example:
        >>> config = PluginConfig()
        >>> version = Version.from_vcs(Vcs.Git, path=".")
        >>> render_jinja_template("v{{ major }}.{{ minor }}.{{ patch }}", version=version, config=config)
        'v1.2.3'
    """
    # Build the default context with version information
    context = {
        # Version object and properties
        "version": version,
        "base": version.base,
        "stage": version.stage,
        "revision": version.revision,
        "distance": version.distance,
        "commit": version.commit,
        "dirty": version.dirty,
        "branch": version.branch,
        "tagged_metadata": version.tagged_metadata,
        # Processed values
        "branch_escaped": _escape_branch(version.branch, config.escape_with),
        "timestamp": _format_timestamp(version.timestamp),
        # Base version parts
        "major": _base_part(version.base, 0),
        "minor": _base_part(version.base, 1),
        "patch": _base_part(version.base, 2),
        # Helper functions
        "bump_version": bump_version,
        "serialize_pep440": serialize_pep440,
        "serialize_pvp": serialize_pvp,
        "serialize_semver": serialize_semver,
    }

    # Add custom imports if configured
    for import_config in config.get_jinja_imports():
        try:
            module = import_module(import_config.module)
        except ImportError as e:
            raise ValueError(
                f"Failed to import module '{import_config.module}': {e}"
            ) from e

        if import_config.item is not None:
            try:
                context[import_config.item] = getattr(module, import_config.item)
            except AttributeError:
                raise ValueError(
                    f"Module '{import_config.module}' has no item '{import_config.item}'"
                ) from None
        else:
            context[import_config.module] = module

    return _JINJA_ENV.from_string(template_str).render(**context)
