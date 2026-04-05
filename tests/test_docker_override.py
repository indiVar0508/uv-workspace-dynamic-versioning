import pytest
from pathlib import Path
from unittest.mock import patch
from dunamai import Version
from uv_workspace_dynamic_versioning.schemas import PluginConfig
from uv_workspace_dynamic_versioning.version_source import get_version

def test_override_and_docker_fallback(tmp_path):
    # Simulate workspace without git (Docker environment)
    root = tmp_path / "workspace"
    root.mkdir()
    
    # Create pyproject.toml with version
    pyproject = root / "pyproject.toml"
    pyproject.write_text("""
[project]
name = "my-workspace"
version = "2.5.0"
""")

    # Package directory
    pkg = root / "packages" / "my-pkg"
    pkg.mkdir(parents=True)
    
    config = PluginConfig(vcs="git")
    
    # get_version should not raise RuntimeError even though git fails,
    # because it will fallback to the workspace version!
    # Wait, _patch_version_for_directory will run git commands and fail silently.
    version_str, version_obj = get_version(config, pkg)
    
    assert version_str == "2.5.0"
    assert version_obj.base == "2.5.0"
    assert version_obj.distance == 0

def test_override_with_git(tmp_path):
    import subprocess
    root = tmp_path / "repo"
    root.mkdir()
    
    subprocess.run(["git", "init"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=root, check=True)
    
    # First commit
    (root / "README.md").write_text("Hello")
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "commit", "-m", "Initial"], cwd=root, check=True)
    subprocess.run(["git", "tag", "v1.0.0"], cwd=root, check=True)
    
    # Root pyproject.toml overriding the version to 2.0.0
    pyproject = root / "pyproject.toml"
    pyproject.write_text("""
[project]
name = "my-workspace"
version = "2.0.0"
""")
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "commit", "-m", "Add pyproject"], cwd=root, check=True)
    
    config = PluginConfig(vcs="git")
    version_str, version_obj = get_version(config, root)
    
    # Distance should be 1, because 1 commit since tag v1.0.0
    # Base should be 2.0.0
    assert version_obj.base == "2.0.0"
    assert version_obj.distance == 1
    assert "2.0.0.post1" in version_str

