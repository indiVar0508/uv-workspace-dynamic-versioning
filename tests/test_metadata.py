"""Tests for the metadata hook."""

from __future__ import annotations

import pytest
from pathlib import Path
from uv_workspace_dynamic_versioning.metadata_hook import DependenciesMetadataHook
from uv_workspace_dynamic_versioning.schemas import MetadataHookConfig


class MockVersion:
    def __init__(self, base, major, minor, patch):
        self.base = base
        self.major = major
        self.minor = minor
        self.patch = patch


@pytest.fixture
def mock_version_obj():
    return MockVersion("1.2.3", 1, 2, 3)


def test_dependency_rendering(tmp_path, monkeypatch):
    """Test that dependencies are correctly rendered with version info."""
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("""
[project]
name = "test"
dynamic = ["version", "dependencies"]

[tool.uv-workspace-dynamic-versioning.dependencies]
dependencies = ["other-pkg=={{ version.base }}", "common~={{ major }}.{{ minor }}"]
""")

    hook = DependenciesMetadataHook(tmp_path, {})

    # Mock get_version to return a version object
    from uv_workspace_dynamic_versioning import version_source
    def mock_get_version(config, root):
        from dunamai import Version
        v = Version("1.2.3")
        return "1.2.3", v

    monkeypatch.setattr(version_source, "get_version", mock_get_version)

    metadata = {"dynamic": ["dependencies"]}
    hook.update(metadata)

    assert "dependencies" in metadata
    assert metadata["dependencies"] == ["other-pkg==1.2.3", "common~=1.2"]


def test_optional_dependency_rendering(tmp_path, monkeypatch):
    """Test that optional dependencies are correctly rendered."""
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("""
[project]
name = "test"
dynamic = ["version", "optional-dependencies"]

[tool.uv-workspace-dynamic-versioning.dependencies]
optional-dependencies = { dev = ["pytest=={{ version.base }}"] }
""")

    hook = DependenciesMetadataHook(tmp_path, {})

    from uv_workspace_dynamic_versioning import version_source
    def mock_get_version(config, root):
        from dunamai import Version
        v = Version("1.2.3")
        return "1.2.3", v

    monkeypatch.setattr(version_source, "get_version", mock_get_version)

    metadata = {"dynamic": ["optional-dependencies"]}
    hook.update(metadata)

    assert "optional-dependencies" in metadata
    assert metadata["optional-dependencies"]["dev"] == ["pytest==1.2.3"]
