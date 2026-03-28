"""Dependencies metadata hook for hatch.

This module provides the DependenciesMetadataHook class that implements
hatch's MetadataHookInterface to enable dynamic dependency resolution
with Jinja2 template rendering.
"""

from __future__ import annotations

from functools import cached_property
from pathlib import Path

from dunamai import Version
from hatchling.metadata.plugin.interface import MetadataHookInterface

from .schemas import MetadataHookConfig, load_metadata_hook_config, load_project_config
from .template import render_jinja_template


class DependenciesMetadataHook(MetadataHookInterface):
    """Metadata hook for dynamic dependency resolution with Jinja2 templating.

    This hook allows you to define dependencies with Jinja2 templates that
    will be rendered with the project version, enabling things like:

    Example configuration:
        [tool.uv-workspace-dynamic-versioning.dependencies]
        dependencies = [
            "mypackage=={{ version }}",
        ]
        optional-dependencies.dev = [
            "pytest~={{ major }}.{{ minor }}",
        ]
    """

    PLUGIN_NAME = "uv-workspace-dynamic-versioning"

    @cached_property
    def hook_config(self) -> MetadataHookConfig:
        """Load and cache the metadata hook configuration."""
        return load_metadata_hook_config(self.root)

    @cached_property
    def version(self) -> Version:
        """Get the project version for template rendering."""
        from .version_source import get_version

        config = load_project_config(self.root)
        _, version = get_version(config, Path(self.root))
        return version

    def render_dependencies(self) -> list[str] | None:
        """Render dependency templates with version information.

        Returns:
            List of rendered dependency strings, or None if not configured
        """
        deps = self.hook_config.dependencies
        if not deps:
            return None

        config = load_project_config(self.root)
        return [render_jinja_template(dep, version=self.version, config=config) for dep in deps]

    def render_optional_dependencies(self) -> dict[str, list[str]] | None:
        """Render optional dependency templates with version information.

        Returns:
            Dictionary mapping group names to rendered dependency lists,
            or None if not configured
        """
        opt_deps = self.hook_config.optional_dependencies
        if not opt_deps:
            return None

        config = load_project_config(self.root)
        return {
            group: [render_jinja_template(dep, version=self.version, config=config) for dep in deps]
            for group, deps in opt_deps.items()
        }

    def update(self, metadata: dict) -> None:
        """Update project metadata with dynamic dependencies.

        This method is called by hatch during the metadata hook phase.
        It validates the configuration and injects rendered dependencies.

        Args:
            metadata: The project metadata dictionary to update

        Raises:
            ValueError: If configuration is invalid or inconsistent
        """
        dynamic = metadata.get("dynamic", [])
        is_dynamic_deps = "dependencies" in dynamic
        is_dynamic_opt_deps = "optional-dependencies" in dynamic

        # Check that dependencies are declared as dynamic
        if not (is_dynamic_deps or is_dynamic_opt_deps):
            raise ValueError(
                "Cannot use this plugin when 'dependencies' or 'optional-dependencies' "
                "is not listed in 'project.dynamic'."
            )

        # Check consistency between dynamic and project
        if is_dynamic_deps and "dependencies" in metadata:
            raise ValueError("'dependencies' is dynamic but already listed in [project].")

        if is_dynamic_opt_deps and "optional-dependencies" in metadata:
            raise ValueError("'optional-dependencies' is dynamic but already listed in [project].")

        # Check that we have something to render
        has_deps = self.hook_config.dependencies is not None
        has_opt_deps = self.hook_config.optional_dependencies is not None
        if not (has_deps or has_opt_deps):
            raise ValueError("No dependencies or optional-dependencies found in the plugin config.")

        # Render and inject dependencies
        rendered_deps = self.render_dependencies()
        if rendered_deps:
            metadata["dependencies"] = rendered_deps

        rendered_opt_deps = self.render_optional_dependencies()
        if rendered_opt_deps:
            metadata["optional-dependencies"] = rendered_opt_deps
