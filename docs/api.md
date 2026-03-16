# API Reference

This page provides an overview of the core components of `uv-workspace-dynamic-versioning`.

## Version Source

::: uv_workspace_dynamic_versioning.plugin.DynamicWorkspaceVersionSource

## Metadata Hook

::: uv_workspace_dynamic_versioning.hooks.hatch_register_metadata_hook
    options:
      show_root_heading: true

## Core Logic

::: uv_workspace_dynamic_versioning.vendored.main.get_version
    options:
      show_root_heading: true

::: uv_workspace_dynamic_versioning.vendored.main.patch_version_for_directory
    options:
      show_root_heading: true

## Error Handling

The plugin may raise the following errors:

*   **`ValueError`**:
    *   When configuration validation fails (e.g., wrong type for an option).
    *   When a `from-file` pattern does not match the file content.
    *   When dynamic dependencies are incorrectly configured in `pyproject.toml`.
    *   When a generated version does not match the specified `style` (e.g., PEP 440).
*   **`RuntimeError`**:
    *   When `dunamai` fails to detect a VCS and no `fallback-version` is provided.
