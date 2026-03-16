from pathlib import Path

from hatchling.version.source.plugin.interface import VersionSourceInterface

from . import schemas
from .base import BasePlugin
from .main import get_version


class DynamicWorkspaceVersionSource(BasePlugin, VersionSourceInterface):
    PLUGIN_NAME = "uv-workspace-dynamic-versioning"

    def get_version_data(self) -> dict[str, str]:
        """
        Retrieves the version data for the project.

        This method is called by Hatch to determine the project version. It parses
        the plugin configuration, retrieves the version from VCS (or other sources),
        and applies directory-specific patching for workspace support.

        Returns:
            dict[str, str]: A dictionary containing the "version" key.
        """
        config = schemas.UvWorkspaceDynamicVersioning.from_dict(self.config)
        version, _ = get_version(config, Path(self.root))
        return {"version": version}
