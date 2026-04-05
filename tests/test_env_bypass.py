from uv_workspace_dynamic_versioning.schemas import PluginConfig
from uv_workspace_dynamic_versioning.version_source import get_version


def test_override_env_var(tmp_path, monkeypatch):
    pkg_dir = tmp_path / "pkg"
    pkg_dir.mkdir()
    
    (pkg_dir / "pyproject.toml").write_text("""
[project]
name = "my-special-package"
""")
    
    # Test global bypass
    monkeypatch.setenv("UV_WORKSPACE_DYNAMIC_VERSIONING_BYPASS", "3.0.0")
    config = PluginConfig()
    
    v_str, v_obj = get_version(config, pkg_dir)
    assert v_str == "3.0.0"
    
    # Test specific override taking precedence
    monkeypatch.setenv("UV_WORKSPACE_DYNAMIC_VERSIONING_OVERRIDE", "other-pkg=1.0.0, my-special-package = 4.5.0")
    
    v_str, v_obj = get_version(config, pkg_dir)
    assert v_str == "4.5.0"
    
    # Test legacy bypass
    monkeypatch.delenv("UV_WORKSPACE_DYNAMIC_VERSIONING_OVERRIDE")
    monkeypatch.delenv("UV_WORKSPACE_DYNAMIC_VERSIONING_BYPASS")
    monkeypatch.setenv("UV_DYNAMIC_VERSIONING_BYPASS", "5.0.0")
    
    v_str, v_obj = get_version(config, pkg_dir)
    assert v_str == "5.0.0"

