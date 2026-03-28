"""
uv-workspace-dynamic-versioning

A dynamic version source plugin for uv workspaces that integrates with hatch's build backend.
"""

from importlib.metadata import version as _get_version

from .plugin import DynamicWorkspaceVersionSource

__all__ = ["DynamicWorkspaceVersionSource"]

try:
    __version__ = _get_version("uv-workspace-dynamic-versioning")
except Exception:
    __version__ = "0.0.0"
