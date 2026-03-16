from __future__ import annotations
from pathlib import Path

from functools import cached_property

from dunamai import Version
from hatchling.metadata.plugin.interface import MetadataHookInterface

from . import schemas
from .base import BasePlugin
from .main import get_version
from .template import render_template


class DependenciesMetadataHook(BasePlugin, MetadataHookInterface):
    """
    Hatch metadata hook to populate `project.dependencies` and `project.optional-dependencies`
    """

    PLUGIN_NAME = "uv-workspace-dynamic-versioning"

    @cached_property
    def plugin_config(self) -> schemas.MetadataHookConfig:
        return schemas.MetadataHookConfig.from_dict(self.config)

    @cached_property
    def version(self) -> Version:
        _, version = get_version(self.project_config, Path(self.root))
        return version

    def render_dependencies(self) -> list[str] | None:
        if self.plugin_config.dependencies is None:
            return None

        return [
            render_template(dep, version=self.version, config=self.project_config)
            for dep in self.plugin_config.dependencies
        ]

    def render_optional_dependencies(self) -> dict[str, list[str]] | None:
        if self.plugin_config.optional_dependencies is None:
            return None

        return {
            name: [
                render_template(dep, version=self.version, config=self.project_config)
                for dep in deps
            ]
            for name, deps in self.plugin_config.optional_dependencies.items()
        }

    def update(self, metadata: dict) -> None:
        """
        Updates the project metadata with dynamic dependencies.

        This method is called by Hatch during the metadata hook phase. It renders
        dependency templates using Jinja2 and injects them into the metadata dictionary.

        Args:
            metadata (dict): The project metadata dictionary.

        Raises:
            ValueError: If 'dependencies' or 'optional-dependencies' are not listed
                as dynamic in pyproject.toml, or if they are already defined in [project].
        """
        # check dynamic
        dynamic = metadata.get("dynamic", [])
        is_dynamic_dependencies = "dependencies" in dynamic
        is_dynamic_optional_dependencies = "optional-dependencies" in dynamic
        if not (is_dynamic_dependencies or is_dynamic_optional_dependencies):
            raise ValueError(
                "Cannot use this plugin when 'dependencies' or 'optional-dependencies' is not listed in 'project.dynamic'."
            )

        # check consistency between dynamic and project
        has_dependencies = "dependencies" in metadata
        if is_dynamic_dependencies and has_dependencies:
            raise ValueError(
                "'dependencies' is dynamic but already listed in [project]."
            )

        has_optional_dependencies = "optional-dependencies" in metadata
        if is_dynamic_optional_dependencies and has_optional_dependencies:
            raise ValueError(
                "'optional-dependencies' is dynamic but already listed in [project]."
            )

        has_dependencies = self.plugin_config.dependencies is not None
        has_optional_dependencies = self.plugin_config.optional_dependencies is not None
        if not (has_dependencies or has_optional_dependencies):
            raise ValueError(
                "No dependencies or optional-dependencies found in the plugin config."
            )

        rendered_dependencies = self.render_dependencies()
        if rendered_dependencies:
            metadata["dependencies"] = rendered_dependencies

        rendered_optional_dependencies = self.render_optional_dependencies()
        if rendered_optional_dependencies:
            metadata["optional-dependencies"] = rendered_optional_dependencies
