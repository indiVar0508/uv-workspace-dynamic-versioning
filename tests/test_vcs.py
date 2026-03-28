"""Tests for VCS integration."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
from dunamai import Version

from uv_workspace_dynamic_versioning.schemas import PluginConfig
from uv_workspace_dynamic_versioning.version_source import get_version


@pytest.fixture
def git_repo(tmp_path):
    """Fixture to create a temporary git repository."""
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()

    subprocess.run(["git", "init"], cwd=repo_dir, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_dir, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_dir, check=True)

    # Initial commit
    (repo_dir / "README.md").write_text("Test")
    subprocess.run(["git", "add", "."], cwd=repo_dir, check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo_dir, check=True)

    return repo_dir


def test_git_tag_detection(git_repo):
    """Test that git tags are correctly detected."""
    subprocess.run(["git", "tag", "v1.0.0"], cwd=git_repo, check=True)

    config = PluginConfig(vcs="git")
    version_str, version_obj = get_version(config, git_repo)

    assert version_str == "1.0.0"
    assert version_obj.base == "1.0.0"
    assert version_obj.distance == 0


def test_git_distance(git_repo):
    """Test that git distance is correctly calculated."""
    subprocess.run(["git", "tag", "v1.0.0"], cwd=git_repo, check=True)

    # Add a commit
    (git_repo / "file.txt").write_text("Hello")
    subprocess.run(["git", "add", "."], cwd=git_repo, check=True)
    subprocess.run(["git", "commit", "-m", "Add file"], cwd=git_repo, check=True)

    config = PluginConfig(vcs="git")
    version_str, version_obj = get_version(config, git_repo)

    assert "1.0.0.post1" in version_str
    assert version_obj.distance == 1


def test_directory_specific_patching(git_repo):
    """Test that distance is filtered by directory."""
    subprocess.run(["git", "tag", "v1.0.0"], cwd=git_repo, check=True)

    # Create two directories
    pkg_a = git_repo / "pkg-a"
    pkg_a.mkdir()
    pkg_b = git_repo / "pkg-b"
    pkg_b.mkdir()

    # Commit in pkg-a
    (pkg_a / "file.txt").write_text("A")
    subprocess.run(["git", "add", "."], cwd=git_repo, check=True)
    subprocess.run(["git", "commit", "-m", "Change in A"], cwd=git_repo, check=True)

    # Commit in pkg-b
    (pkg_b / "file.txt").write_text("B")
    subprocess.run(["git", "add", "."], cwd=git_repo, check=True)
    subprocess.run(["git", "commit", "-m", "Change in B"], cwd=git_repo, check=True)

    config = PluginConfig(vcs="git")

    # pkg-a should have distance 1
    version_a, obj_a = get_version(config, pkg_a)
    assert obj_a.distance == 1

    # pkg-b should have distance 1 (not 2!)
    version_b, obj_b = get_version(config, pkg_b)
    assert obj_b.distance == 1


def test_dirty_state(git_repo):
    """Test dirty state detection."""
    subprocess.run(["git", "tag", "v1.0.0"], cwd=git_repo, check=True)

    # Modify a file but don't commit
    (git_repo / "README.md").write_text("Dirty")

    config = PluginConfig(vcs="git")
    version_str, version_obj = get_version(config, git_repo)

    assert "dirty" in version_str
    assert version_obj.dirty is True


def test_bump_logic(git_repo):
    """Test version bumping logic."""
    subprocess.run(["git", "tag", "v1.0.0"], cwd=git_repo, check=True)

    # Add a commit
    (git_repo / "file.txt").write_text("Hello")
    subprocess.run(["git", "add", "."], cwd=git_repo, check=True)
    subprocess.run(["git", "commit", "-m", "Add file"], cwd=git_repo, check=True)

    config = PluginConfig(vcs="git", bump=True)
    version_str, version_obj = get_version(config, git_repo)

    # 1.0.0 -> bumped to 1.0.1
    assert "1.0.1" in version_str
    assert version_obj.base == "1.0.1"
