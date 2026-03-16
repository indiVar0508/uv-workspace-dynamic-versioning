from pathlib import Path
from hatchling.version.source.plugin.interface import VersionSourceInterface

from .base import BasePlugin
from .main import get_version


class DynamicWorkspaceVersionSource(BasePlugin, VersionSourceInterface):
    PLUGIN_NAME = "uv-workspace-dynamic-versioning"

    def get_version_data(self) -> dict[str, str]:
        version, _ = get_version(self.project_config, Path(self.root))
        return {"version": version}
