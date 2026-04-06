"""Tests to reach 100% coverage."""

from __future__ import annotations

from pathlib import Path

import pytest
from dunamai import Style, Vcs, Version

from uv_workspace_dynamic_versioning import hooks, plugin
from uv_workspace_dynamic_versioning.metadata_hook import DependenciesMetadataHook
from uv_workspace_dynamic_versioning.schemas import (
    BumpConfig,
    FormatJinjaImport,
    FromFileConfig,
    MetadataHookConfig,
    PluginConfig,
    load_metadata_hook_config,
    load_project_config,
)
from uv_workspace_dynamic_versioning.template import render_jinja_template
from uv_workspace_dynamic_versioning.version_source import (
    DynamicWorkspaceVersionSource,
    _read_version_from_file,
    get_version,
)


def test_hooks_registration():
    """Test hatch registration hooks."""
    assert hooks.hatch_register_version_source() == DynamicWorkspaceVersionSource
    assert hooks.hatch_register_metadata_hook() == DependenciesMetadataHook


def test_plugin_version():
    """Test plugin module exports."""
    assert plugin.__name__ == "uv_workspace_dynamic_versioning.plugin"


def test_metadata_hook_error_cases(tmp_path):
    """Test error cases for metadata hook."""
    hook = DependenciesMetadataHook(tmp_path, {})

    # No dynamic dependencies declared
    metadata = {"dynamic": []}
    with pytest.raises(ValueError, match="Cannot use this plugin"):
        hook.update(metadata)


def test_schemas_errors(tmp_path):
    """Test schema loading error cases."""
    # Invalid TOML
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("invalid = [")
    # Should not raise ValueError for parse, but might fail during load_toml
    # actually my load_project_config catches Exception and returns default if it can't parse
    # but let's check what it actually does
    res = load_project_config(tmp_path)
    assert isinstance(res, PluginConfig)

    # Missing pyproject
    with pytest.raises(FileNotFoundError):
        load_project_config("/nonexistent")

    # load_metadata_hook_config with missing file
    assert isinstance(load_metadata_hook_config("/nonexistent"), MetadataHookConfig)


def test_from_file_version(tmp_path):
    """Test reading version from file."""
    version_file = tmp_path / "VERSION"
    version_file.write_text("1.2.3")

    from uv_workspace_dynamic_versioning.schemas import FromFileConfig, PluginConfig
    config = PluginConfig(from_file=FromFileConfig(source="VERSION"))
    v_str, v_obj = get_version(config, tmp_path)
    assert v_str == "1.2.3"
    assert v_obj.base == "1.2.3"

    # With pattern
    config = PluginConfig(from_file=FromFileConfig(source="VERSION", pattern=r"version = (.+)"))
    version_file.write_text("version = 2.3.4")
    v_str, v_obj = get_version(config, tmp_path)
    assert v_str == "2.3.4"

    # Pattern doesn't match
    config = PluginConfig(from_file=FromFileConfig(source="VERSION", pattern=r"nomatch"))
    with pytest.raises(ValueError, match="Pattern 'nomatch' did not match"):
        _read_version_from_file(config, tmp_path)

    # Security: outside root
    config = PluginConfig(from_file=FromFileConfig(source="../VERSION"))
    with pytest.raises(ValueError, match="is outside of the project root"):
        _read_version_from_file(config, tmp_path)


def test_from_file_config_validation():
    """Test FromFileConfig validation."""
    # Valid
    c = FromFileConfig(source="V")
    assert c.source == "V"


def test_jinja_template_parts():
    """Test Jinja template rendering of version parts."""
    version = Version("1.2.3", distance=5, commit="abc", branch="feat/test")
    config = PluginConfig()

    template = "{{ major }}.{{ minor }}.{{ patch }} ({{ branch_escaped }})"
    result = render_jinja_template(template, version=version, config=config)
    assert result == "1.2.3 (feattest)"

    # Test with custom module import
    config = PluginConfig(format_jinja_imports=[FormatJinjaImport(module="os", item="name")])
    result = render_jinja_template("{{ name }}", version=version, config=config)
    assert result in ["posix", "nt"]

    # Import module without item
    config = PluginConfig(format_jinja_imports=[FormatJinjaImport(module="math")])
    result = render_jinja_template("{{ math.sqrt(16) }}", version=version, config=config)
    assert result == "4.0"


def test_version_style_pvp():
    """Test PVP version style."""
    from uv_workspace_dynamic_versioning.version_source import check_version_style

    check_version_style("1.2.3", Style.Pvp)
    with pytest.raises(ValueError, match="does not conform to Pvp style"):
        check_version_style("invalid", Style.Pvp)


def test_vcs_fallback(tmp_path):
    """Test VCS fallback when no VCS is found."""
    config = PluginConfig(fallback_version="0.1.0")
    # tmp_path is not a git repo
    v_str, v_obj = get_version(config, tmp_path)
    assert v_str == "0.1.0"


def test_schemas_normalization_more():
    """Test more schema normalization cases."""
    from uv_workspace_dynamic_versioning.schemas import parse_project_config

    # Already a Vcs object
    config = PluginConfig(vcs=Vcs.Git)
    assert config.vcs == Vcs.Git

    # Invalid Vcs string via parser
    config = parse_project_config({"vcs": "invalid"})
    assert config.vcs == Vcs.Any

    # Already a Style object
    config = PluginConfig(style=Style.SemVer)
    assert config.style == Style.SemVer

    # Invalid style string via parser
    config = parse_project_config({"style": "invalid"})
    assert config.style is None

    # Already a BumpConfig object
    bump_obj = BumpConfig(enable=True)
    config = PluginConfig(bump=bump_obj)
    assert config.bump == bump_obj

    # BumpConfig from dict via parser
    config = parse_project_config({"bump": {"enable": True, "index": 0}})
    assert isinstance(config.bump, BumpConfig)
    assert config.bump.enable is True

    # from_file from dict via parser
    config = parse_project_config({"from-file": {"source": "VERSION"}})
    assert isinstance(config.from_file, FromFileConfig)
    assert config.get_from_file().source == "VERSION"

    # get_jinja_imports with objects
    imp = FormatJinjaImport(module="math")
    config = PluginConfig(format_jinja_imports=[imp])
    assert config.get_jinja_imports() == [imp]

    # normalize_config_keys with list
    from uv_workspace_dynamic_versioning.schemas import normalize_config_keys

    data = {"my-list": [{"a-b": 1}]}
    norm = normalize_config_keys(data)
    assert norm["my_list"][0]["a_b"] == 1


def test_schemas_errors_extra(tmp_path):
    """Test more schema error cases."""

    # load_metadata_hook_config with invalid file
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("invalid")
    assert isinstance(load_metadata_hook_config(tmp_path), MetadataHookConfig)


def test_metadata_hook_config_validator():
    """Test MetadataHookConfig validator directly."""
    # Valid
    c = MetadataHookConfig(dependencies=["a"])
    assert c.dependencies == ["a"]

    # None
    c = MetadataHookConfig(dependencies=None)
    assert c.dependencies is None


def test_normalize_config_list():
    """Test normalize_config_keys with list of dicts."""
    from uv_workspace_dynamic_versioning.schemas import normalize_config_keys

    data = {"a-b": [{"c-d": 1}]}
    res = normalize_config_keys(data)
    assert res["a_b"][0]["c_d"] == 1


def test_jinja_imports_validation():
    """Test Jinja imports validation in PluginConfig."""

    from uv_workspace_dynamic_versioning.schemas import parse_project_config
    # Valid dict import via parser
    c = parse_project_config({"format-jinja-imports": [{"module": "os", "item": "path"}]})
    imps = c.get_jinja_imports()
    assert imps[0].module == "os"
    assert imps[0].item == "path"

    # Valid object import
    obj = FormatJinjaImport(module="sys")
    c = PluginConfig(format_jinja_imports=[obj])
    assert c.get_jinja_imports()[0].module == "sys"


def test_template_error_handling():
    """Test Jinja template error cases."""
    from uv_workspace_dynamic_versioning.schemas import FormatJinjaImport
    from uv_workspace_dynamic_versioning.template import render_jinja_template

    v = Version("1.0.0")

    # Missing module
    c = PluginConfig(format_jinja_imports=[FormatJinjaImport(module="nonexistent_module_xyz")])
    with pytest.raises(ValueError, match="Failed to import module"):
        render_jinja_template("{{ version }}", version=v, config=c)

    # Missing item in module
    c = PluginConfig(format_jinja_imports=[FormatJinjaImport(module="os", item="nonexistent_item")])
    with pytest.raises(ValueError, match="has no item"):
        render_jinja_template("{{ version }}", version=v, config=c)


def test_version_source_more(tmp_path, monkeypatch):
    """Test more version source cases."""
    from uv_workspace_dynamic_versioning.schemas import FromFileConfig
    # Bypass
    monkeypatch.setenv("UV_DYNAMIC_VERSIONING_BYPASS", "1.1.1")
    v_str, v_obj = get_version(PluginConfig(), tmp_path)
    assert v_str == "1.1.1"
    monkeypatch.delenv("UV_DYNAMIC_VERSIONING_BYPASS")

    # from_file without pattern
    version_file = tmp_path / "VERSION"
    version_file.write_text("5.5.5")
    config = PluginConfig(from_file=FromFileConfig(source="VERSION"))
    v_str = _read_version_from_file(config, tmp_path)
    assert v_str == "5.5.5"

    # No tags found warning
    # We mock Version.from_vcs to return 0.0.0
    from dunamai import Version as DunamaiVersion

    def mock_from_vcs(*args, **kwargs):
        return DunamaiVersion("0.0.0")

    monkeypatch.setattr(DunamaiVersion, "from_vcs", mock_from_vcs)
    config = PluginConfig()
    # Should print to stderr but we just check it runs
    v_str, v_obj = get_version(config, tmp_path)
    assert v_obj.base == "0.0.0"


def test_patch_error(tmp_path):
    """Test error handling in directory patching."""
    from uv_workspace_dynamic_versioning.version_source import _patch_version_for_directory

    v = Version("1.0.0")
    # Using a path that is not a git repo to trigger exception
    # (though subprocess might just fail)
    res = _patch_version_for_directory(v, Path("/nonexistent"))
    assert res == v
