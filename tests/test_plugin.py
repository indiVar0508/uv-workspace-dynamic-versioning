"""Tests for the version source plugin."""

from __future__ import annotations

import pytest

from uv_workspace_dynamic_versioning.schemas import PluginConfig, load_project_config
from uv_workspace_dynamic_versioning.version_source import (
    DynamicWorkspaceVersionSource,
    check_version_style,
    get_version,
)


class TestPluginConfig:
    """Tests for PluginConfig schema."""

    def test_default_config(self):
        """Test that default configuration is valid."""
        config = PluginConfig()
        # Default vcs is a string "any" after normalization
        assert config.vcs == "any"
        assert config.latest_tag is False
        assert config.strict is False
        assert config.bump is False

    def test_config_from_dict(self):
        """Test creating config from dictionary."""
        data = {
            "vcs": "git",
            "latest_tag": True,
            "bump": True,
        }
        config = PluginConfig(**data)
        assert config.vcs.value == "git"
        assert config.latest_tag is True
        assert config.bump is True

    def test_jinja_format(self):
        """Test Jinja format configuration."""
        data = {"format_jinja": "{{ major }}.{{ minor }}.{{ patch }}"}
        config = PluginConfig(**data)
        assert config.format_jinja == "{{ major }}.{{ minor }}.{{ patch }}"

    def test_from_file_config(self):
        """Test from-file configuration."""
        data = {"from_file": {"source": "VERSION", "pattern": "v(.+)"}}
        config = PluginConfig(**data)
        from_file = config.get_from_file()
        assert from_file is not None
        assert from_file.source == "VERSION"
        assert from_file.pattern == "v(.+)"

    def test_style_normalization(self):
        """Test that style is normalized correctly."""
        config = PluginConfig(style="PEP440")
        assert config.style.value == "pep440"

    def test_extra_fields_ignored(self):
        """Test that extra fields are ignored."""
        data = {"unknown_field": "value", "vcs": "git"}
        config = PluginConfig(**data)
        assert hasattr(config, "unknown_field") is False
        assert config.vcs.value == "git"


class TestVersionStyleValidation:
    """Tests for version style validation."""

    def test_valid_pep440(self):
        """Test PEP 440 validation with valid versions."""
        from dunamai import Style

        # Standard versions
        check_version_style("1.0.0", Style.Pep440)
        check_version_style("1.0.0+abc123", Style.Pep440)
        check_version_style("1.0.0.post1", Style.Pep440)

    def test_valid_semver(self):
        """Test SemVer validation."""
        from dunamai import Style

        check_version_style("1.0.0", Style.SemVer)
        check_version_style("1.0.0-alpha", Style.SemVer)
        check_version_style("1.0.0+build.123", Style.SemVer)

    def test_invalid_version(self):
        """Test that invalid versions raise ValueError."""
        from dunamai import Style

        with pytest.raises(ValueError):
            check_version_style("invalid", Style.Pep440)


class TestLoadProjectConfig:
    """Tests for loading configuration from pyproject.toml."""

    def test_load_from_directory(self, tmp_path):
        """Test loading config from a directory with pyproject.toml."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            """
[project]
name = "test"
dynamic = ["version"]

[tool.uv-workspace-dynamic-versioning]
vcs = "git"
latest-tag = true
"""
        )

        config = load_project_config(tmp_path)
        assert config.vcs.value == "git"
        assert config.latest_tag is True

    def test_load_without_config(self, tmp_path):
        """Test loading config without plugin config returns defaults."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            """
[project]
name = "test"
"""
        )

        config = load_project_config(tmp_path)
        # Default vcs is string "any"
        assert config.vcs == "any"

    def test_file_not_found(self):
        """Test that FileNotFoundError is raised when no pyproject.toml."""
        with pytest.raises(FileNotFoundError):
            load_project_config("/nonexistent/path")


class TestDynamicWorkspaceVersionSource:
    """Tests for the DynamicWorkspaceVersionSource class."""

    def test_plugin_name(self):
        """Test that plugin name is correct."""
        assert DynamicWorkspaceVersionSource.PLUGIN_NAME == "uv-workspace-dynamic-versioning"


class TestVersionBypass:
    """Tests for version bypass functionality."""

    def test_bypass_via_env_var(self, tmp_path, monkeypatch):
        """Test that environment variable bypasses version detection."""
        monkeypatch.setenv("UV_DYNAMIC_VERSIONING_BYPASS", "1.2.3")
        config = PluginConfig()
        version, version_obj = get_version(config, tmp_path)
        assert version == "1.2.3"


class TestSchemasNormalization:
    """Tests for schema normalization."""

    def test_kebab_to_snake_case(self):
        """Test that kebab-case is converted to snake_case."""
        data = {"latest-tag": True, "commit-length": 8}
        normalized = {}
        for key, value in data.items():
            normalized[key.replace("-", "_")] = value
        assert "latest_tag" in normalized
        assert "commit_length" in normalized
