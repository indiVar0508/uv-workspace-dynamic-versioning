"""Configuration schemas using Pydantic for validation.

This module provides type-safe configuration schemas for the plugin,
supporting both kebab-case (TOML) and snake_case (Python) field names.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from dunamai import Style, Vcs
from pydantic import BaseModel, Field, field_validator


class BumpConfig(BaseModel):
    """Configuration for automatic version bumping."""

    enable: bool = False
    index: int = Field(default=-1, ge=-1, le=10)

    model_config = {"extra": "ignore"}


class FromFileConfig(BaseModel):
    """Configuration for reading version from a file."""

    source: str
    pattern: str | None = None

    @field_validator("source")
    @classmethod
    def source_must_be_string(cls, v: Any) -> str:
        if not isinstance(v, str):
            raise TypeError("source must be a string")
        return v

    model_config = {"extra": "ignore"}


class FormatJinjaImport(BaseModel):
    """Configuration for Jinja template imports."""

    module: str
    item: str | None = None

    model_config = {"extra": "ignore"}


class PluginConfig(BaseModel):
    """Main configuration for the uv-workspace-dynamic-versioning plugin.

    This schema validates the [tool.uv-workspace-dynamic-versioning] section
    of pyproject.toml and provides sensible defaults for all options.

    All fields support kebab-case (TOML style) and snake_case (Python style)
    for maximum flexibility.
    """

    # VCS settings
    vcs: Vcs | str = "any"
    latest_tag: bool = False
    strict: bool = False
    tag_dir: str = "tags"
    tag_branch: str | None = None
    full_commit: bool = False
    ignore_untracked: bool = False
    commit_length: int | None = Field(default=None, ge=4, le=40)
    commit_prefix: str | None = None

    # Pattern matching
    pattern: str = "default"
    pattern_prefix: str | None = None

    # Version format
    format: str | None = None
    format_jinja: str | None = None
    format_jinja_imports: list[FormatJinjaImport | dict[str, Any]] | None = None
    style: Style | str | None = None

    # Metadata
    metadata: bool | None = None
    tagged_metadata: bool = False
    escape_with: str | None = None

    # Bumping
    bump: BumpConfig | bool = False

    # Fallback
    fallback_version: str | None = None
    dirty: bool | None = None

    # From file
    from_file: FromFileConfig | dict[str, Any] | None = None

    @field_validator("vcs", mode="after")
    @classmethod
    def normalize_vcs(cls, v: Vcs | str) -> Vcs:
        if isinstance(v, Vcs):
            return v
        if isinstance(v, str):
            try:
                return Vcs(v.lower())
            except ValueError:
                return Vcs.Any
        return Vcs.Any

    @field_validator("style", mode="after")
    @classmethod
    def normalize_style(cls, v: Style | str | None) -> Style | None:
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

    @field_validator("bump", mode="after")
    @classmethod
    def normalize_bump(cls, v: BumpConfig | bool | dict[str, Any]) -> BumpConfig | bool:
        if isinstance(v, BumpConfig):
            return v
        if isinstance(v, bool):
            return v
        if isinstance(v, dict):
            return BumpConfig(**{k.replace("-", "_"): val for k, val in v.items()})
        return False

    @field_validator("from_file", mode="after")
    @classmethod
    def normalize_from_file(cls, v: FromFileConfig | dict[str, Any] | None) -> FromFileConfig | dict[str, Any] | None:
        if v is None:
            return None
        if isinstance(v, FromFileConfig):
            return v
        if isinstance(v, dict):
            return v
        return None

    @field_validator("format_jinja_imports", mode="after")
    @classmethod
    def normalize_imports(cls, v: Any) -> list[dict[str, Any]] | None:
        if v is None:
            return None
        if not isinstance(v, list):
            return None
        return v

    @property
    def bump_config(self) -> BumpConfig:
        """Get the bump configuration, with defaults applied."""
        if isinstance(self.bump, BumpConfig):
            return self.bump
        if self.bump is True:
            return BumpConfig(enable=True)
        return BumpConfig()

    def get_from_file(self) -> FromFileConfig | None:
        """Get the from-file configuration, with defaults applied."""
        if self.from_file is None:
            return None
        if isinstance(self.from_file, dict):
            return FromFileConfig(**{k.replace("-", "_"): v for k, v in self.from_file.items()})
        return self.from_file

    def get_jinja_imports(self) -> list[FormatJinjaImport]:
        """Get the Jinja imports, with defaults applied."""
        if not self.format_jinja_imports:
            return []
        imports = []
        for item in self.format_jinja_imports:
            if isinstance(item, dict):
                imports.append(FormatJinjaImport(**{k.replace("-", "_"): v for k, v in item.items()}))
            elif isinstance(item, FormatJinjaImport):
                imports.append(item)
        return imports

    model_config = {
        "extra": "ignore",
        "populate_by_name": True,
        "validate_default": True,
    }


class MetadataHookConfig(BaseModel):
    """Configuration for the dependencies metadata hook.

    This schema validates the [tool.uv-workspace-dynamic-versioning.dependencies]
    section for dynamic dependency resolution.
    """

    dependencies: list[str] | None = None
    optional_dependencies: dict[str, list[str]] | None = None

    @field_validator("dependencies", "optional_dependencies")
    @classmethod
    def validate_lists(cls, v: Any) -> Any:
        if v is None:
            return None
        if not isinstance(v, (list, dict)):
            raise TypeError(f"Expected list or dict, got {type(v).__name__}")
        return v

    model_config = {"extra": "ignore"}


def normalize_config(data: dict[str, Any]) -> dict[str, Any]:
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
            result[normalized_key] = normalize_config(value)
        elif isinstance(value, list):
            result[normalized_key] = [normalize_config(item) if isinstance(item, dict) else item for item in value]
        else:
            result[normalized_key] = value

    return result


def load_project_config(root: Path | str) -> PluginConfig:
    """Load and validate the plugin configuration from pyproject.toml.

    Args:
        root: The project root directory

    Returns:
        Validated PluginConfig instance

    Raises:
        FileNotFoundError: If pyproject.toml doesn't exist
        ValueError: If configuration is invalid
    """
    root = Path(root)
    pyproject_path = root / "pyproject.toml"

    if not pyproject_path.exists():
        raise FileNotFoundError(f"pyproject.toml not found in {root}")

    try:
        import tomlkit

        content = pyproject_path.read_text()
        data = tomlkit.parse(content)
    except Exception as e:
        raise ValueError(f"Failed to parse pyproject.toml: {e}") from e

    # Navigate to tool.uv-workspace-dynamic-versioning
    tool = data.get("tool", {})
    config_data = tool.get("uv-workspace-dynamic-versioning", {})

    # Also check [tool.uv.version] for compatibility
    if not config_data:
        uv_tool = tool.get("uv", {})
        config_data = uv_tool.get("version", {})

    normalized = normalize_config(config_data)
    return PluginConfig(**normalized)


def load_metadata_hook_config(root: Path | str) -> MetadataHookConfig:
    """Load and validate the metadata hook configuration from pyproject.toml.

    Args:
        root: The project root directory

    Returns:
        Validated MetadataHookConfig instance
    """
    root = Path(root)
    pyproject_path = root / "pyproject.toml"

    if not pyproject_path.exists():
        return MetadataHookConfig()

    try:
        import tomlkit

        content = pyproject_path.read_text()
        data = tomlkit.parse(content)
    except Exception:
        return MetadataHookConfig()

    # Navigate to tool.uv-workspace-dynamic-versioning.dependencies
    tool = data.get("tool", {})
    plugin_config = tool.get("uv-workspace-dynamic-versioning", {})
    deps_config = plugin_config.get("dependencies", {})

    normalized = normalize_config(deps_config)
    return MetadataHookConfig(**normalized)
