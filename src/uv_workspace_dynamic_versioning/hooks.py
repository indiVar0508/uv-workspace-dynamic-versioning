"""Hatch plugin hooks for version source and metadata hooks."""

from hatchling.plugin import hookimpl

from .metadata_hook import DependenciesMetadataHook
from .version_source import DynamicWorkspaceVersionSource


@hookimpl
def hatch_register_version_source() -> type[DynamicWorkspaceVersionSource]:
    """Register the dynamic workspace version source plugin with hatch."""
    return DynamicWorkspaceVersionSource


@hookimpl
def hatch_register_metadata_hook() -> type[DependenciesMetadataHook]:
    """Register the dependencies metadata hook plugin with hatch."""
    return DependenciesMetadataHook
