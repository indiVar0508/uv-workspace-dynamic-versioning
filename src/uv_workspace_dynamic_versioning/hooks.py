from hatchling.plugin import hookimpl

from .plugin import DynamicWorkspaceVersionSource
from .vendored.metadata_hook import DependenciesMetadataHook


@hookimpl
def hatch_register_version_source():
    return DynamicWorkspaceVersionSource

@hookimpl
def hatch_register_metadata_hook():
    return DependenciesMetadataHook
