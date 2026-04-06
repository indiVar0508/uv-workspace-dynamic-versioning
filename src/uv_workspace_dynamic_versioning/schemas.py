"""Configuration schemas using standard library dataclasses.

This module provides type-safe configuration schemas for the plugin,
supporting both kebab-case (TOML) and snake_case (Python) field names
without requiring Pydantic.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from dunamai import Style, Vcs

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        # Fallback for environments where tomli isn't installed yet
        # (though it should be a dependency)
        tomllib = None


@dataclass
class BumpConfig:
    """Configuration for automatic version bumping."""

    enable: bool = False
    index: int = -1


@dataclass
class FromFileConfig:
    """Configuration for reading version from a file."""

    source: str
    pattern: str | None = None


@dataclass
class FormatJinjaImport:
    """Configuration for Jinja template imports."""

    module: str
    item: str | None = None


@dataclass
class PluginConfig:
    """Main configuration for the uv-workspace-dynamic-versioning plugin.

    This schema stores the [tool.uv-workspace-dynamic-versioning] section
    of pyproject.toml and provides sensible defaults for all options.
    """

    # VCS settings
    vcs: Vcs = Vcs.Any
    latest_tag: bool = False
    strict: bool = False
    tag_dir: str = "tags"
    tag_branch: str | None = None
    full_commit: bool = False
    ignore_untracked: bool = False
    commit_length: int | None = None
    commit_prefix: str | None = None

    # Pattern matching
    pattern: str = "default"
    pattern_prefix: str | None = None

    # Version format
    format: str | None = None
    format_jinja: str | None = None
    format_jinja_imports: list[FormatJinjaImport] = field(default_factory=list)
    style: Style | None = None

    # Metadata
    metadata: bool | None = None
    tagged_metadata: bool = False
    escape_with: str | None = None

    # Bumping
    bump: BumpConfig = field(default_factory=BumpConfig)

    # Fallback
    fallback_version: str | None = None
    dirty: bool | None = None

    # From file
    from_file: FromFileConfig | None = None

    def __post_init__(self) -> None:
        """Handle type conversions for dataclass initialization."""
        self.vcs = _parse_vcs(self.vcs)
        self.style = _parse_style(self.style)
        self.bump = _parse_bump(self.bump)
        if self.from_file is not None and not isinstance(self.from_file, FromFileConfig):
            self.from_file = _parse_from_file(self.from_file)
        if self.format_jinja_imports and any(not isinstance(i, FormatJinjaImport) for i in self.format_jinja_imports):
            self.format_jinja_imports = _parse_jinja_imports(self.format_jinja_imports)

    @property
    def bump_config(self) -> BumpConfig:
        """Get the bump configuration, for compatibility with old API."""
        return self.bump

    def get_from_file(self) -> FromFileConfig | None:
        """Get the from-file configuration, for compatibility with old API."""
        return self.from_file

    def get_jinja_imports(self) -> list[FormatJinjaImport]:
        """Get the Jinja imports, for compatibility with old API."""
        return self.format_jinja_imports


@dataclass
class MetadataHookConfig:
    """Configuration for the dependencies metadata hook."""

    dependencies: list[str] | None = None
    optional_dependencies: dict[str, list[str]] | None = None


def normalize_config_keys(data: dict[str, Any]) -> dict[str, Any]:
    """Normalize configuration dictionary by converting kebab-case to snake_case.

    Args:
        data: Raw configuration dictionary from pyproject.toml

    Returns:
        Normalized dictionary with snake_case keys
    """
    if not isinstance(data, dict):
        return {}

    result = {}
    for key, value in data.items():
        normalized_key = key.replace("-", "_")

        if isinstance(value, dict):
            result[normalized_key] = normalize_config_keys(value)
        elif isinstance(value, list):
            result[normalized_key] = [
                normalize_config_keys(item) if isinstance(item, dict) else item for item in value
            ]
        else:
            result[normalized_key] = value

    return result


def _parse_vcs(v: Any) -> Vcs:
    if isinstance(v, Vcs):
        return v
    if isinstance(v, str):
        try:
            return Vcs(v.lower())
        except ValueError:
            return Vcs.Any
    return Vcs.Any


def _parse_style(v: Any) -> Style | None:
    if v is None:
        return None
    if isinstance(v, Style):
        return v
    if isinstance(v, str):
        try:
            return Style(v.lower())
        except ValueError:
            return None
    return None


def _parse_bump(v: Any) -> BumpConfig:
    if isinstance(v, BumpConfig):
        return v
    if isinstance(v, bool):
        return BumpConfig(enable=v)
    if isinstance(v, dict):
        return BumpConfig(
            enable=v.get("enable", False),
            index=v.get("index", -1),
        )
    return BumpConfig()


def _parse_from_file(v: Any) -> FromFileConfig | None:
    if v is None:
        return None
    if isinstance(v, FromFileConfig):
        return v
    if isinstance(v, dict) and "source" in v:
        return FromFileConfig(
            source=str(v["source"]),
            pattern=v.get("pattern"),
        )
    return None


def _parse_jinja_imports(v: Any) -> list[FormatJinjaImport]:
    if not isinstance(v, list):
        return []
    imports = []
    for item in v:
        if isinstance(item, dict) and "module" in item:
            imports.append(FormatJinjaImport(module=item["module"], item=item.get("item")))
        elif isinstance(item, FormatJinjaImport):
            imports.append(item)
    return imports


def parse_project_config(data: dict[str, Any]) -> PluginConfig:
    """Parse a normalized dictionary into a PluginConfig instance."""
    data = normalize_config_keys(data)

    # Handle special types and nested objects
    if "vcs" in data:
        data["vcs"] = _parse_vcs(data["vcs"])
    if "style" in data:
        data["style"] = _parse_style(data["style"])
    if "bump" in data:
        data["bump"] = _parse_bump(data["bump"])
    if "from_file" in data:
        data["from_file"] = _parse_from_file(data["from_file"])
    if "format_jinja_imports" in data:
        data["format_jinja_imports"] = _parse_jinja_imports(data["format_jinja_imports"])

    # Create PluginConfig, ignoring extra keys
    valid_keys = PluginConfig.__dataclass_fields__.keys()
    filtered_data = {k: v for k, v in data.items() if k in valid_keys}
    return PluginConfig(**filtered_data)


def load_toml(path: Path) -> dict[str, Any]:
    """Load a TOML file using the best available parser."""
    if tomllib is None:
        raise ImportError("No TOML parser available. Please install 'tomli'.")
    return tomllib.loads(path.read_text(encoding="utf-8"))


def load_project_config(root: Path | str) -> PluginConfig:
    """Load and validate the plugin configuration from pyproject.toml.

    Args:
        root: The project root directory

    Returns:
        PluginConfig instance
    """
    root = Path(root)
    pyproject_path = root / "pyproject.toml"

    if not pyproject_path.exists():
        raise FileNotFoundError(f"pyproject.toml not found in {root}")

    try:
        data = load_toml(pyproject_path)
    except Exception:
        return PluginConfig()

    # Navigate to tool.uv-workspace-dynamic-versioning
    tool = data.get("tool", {})
    config_data = tool.get("uv-workspace-dynamic-versioning", {})

    # Also check [tool.uv.version] for compatibility
    if not config_data:
        uv_tool = tool.get("uv", {})
        config_data = uv_tool.get("version", {})

    return parse_project_config(config_data)


def load_metadata_hook_config(root: Path | str) -> MetadataHookConfig:
    """Load and validate the metadata hook configuration from pyproject.toml.

    Args:
        root: The project root directory

    Returns:
        MetadataHookConfig instance
    """
    root = Path(root)
    pyproject_path = root / "pyproject.toml"

    if not pyproject_path.exists():
        return MetadataHookConfig()

    try:
        data = load_toml(pyproject_path)
    except Exception:
        return MetadataHookConfig()

    # Navigate to tool.uv-workspace-dynamic-versioning.dependencies
    tool = data.get("tool", {})
    plugin_config = tool.get("uv-workspace-dynamic-versioning", {})
    deps_config = plugin_config.get("dependencies", {})

    normalized = normalize_config_keys(deps_config)
    valid_keys = MetadataHookConfig.__dataclass_fields__.keys()
    filtered_data = {k: v for k, v in normalized.items() if k in valid_keys}
    return MetadataHookConfig(**filtered_data)
