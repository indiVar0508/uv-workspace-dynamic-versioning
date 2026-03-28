# refactor-v2

**Purpose:** Refactor codebase with Pydantic schemas, create examples, document backend support

---

## Commit e9f2a6b4 | 2026-03-28T17:26:02.516Z

### Branch Purpose

Refactor the codebase to use Pydantic v2 for robust schema validation, improve project organization by removing the vendored directory, and provide comprehensive documentation and examples for better developer experience.

### Previous Progress Summary

Initial commit.

### This Commit's Contribution

- Migrated configuration management from dataclasses to Pydantic v2, enabling robust validation and seamless support for both kebab-case (TOML) and snake_case (Python) field names.
- Restructured the project by removing the `vendored/` directory and consolidating logic into five top-level modules: `schemas`, `version_source`, `metadata_hook`, `template`, and `hooks`.
- Implemented a sandboxed Jinja2 template rendering environment for safe and flexible version and dependency string formatting.
- Fixed the PEP 440 regex pattern for version validation and bumped the minimum Python requirement to 3.9+ for modern type hinting support.
- Created five comprehensive example projects covering basic setup, monorepo workspaces, Jinja2 templating, dynamic dependency resolution, and custom version formats.
- Added detailed documentation on backend support matrices and best practices for security and CI/CD integration.
- Verified full compatibility and end-to-end functionality with both `hatch build` and `uv build` for single packages and multi-package workspaces.

---

## Commit 9723034d | 2026-03-28T17:50:56.823Z

### Branch Purpose

Refactor the codebase to use Pydantic v2 for robust schema validation, improve project organization, and provide comprehensive documentation and examples for better developer experience.

### Previous Progress Summary

The branch was initialized to migrate configuration management from dataclasses to Pydantic v2, enabling robust validation and support for both kebab-case (TOML) and snake_case (Python) field names. The project was restructured by removing the `vendored/` directory and consolidating logic into five top-level modules. A sandboxed Jinja2 template rendering environment was implemented for safe formatting. The PEP 440 regex pattern for version validation was fixed, and the minimum Python requirement was bumped to 3.9+. Five example projects were created covering basic setup, monorepos, templating, dynamic dependencies, and custom formats. Detailed documentation on backend support and best practices was added, and compatibility with `hatch build` and `uv build` was verified for both single packages and workspaces.

### This Commit's Contribution

- Improved version detection logic by adding a warning when no tags are found, helping users debug "0.0.0" version issues caused by pattern mismatches.
- Fixed a bug in directory-specific patching related to incorrect commit length handling during version serialization.
- Created `examples/06-hybrid-workspace` to demonstrate a complex setup using both `uv-dynamic-versioning` at the root and `uv-workspace-dynamic-versioning` for workspace members.
- Added `scripts/validate_build.py`, an automated CI validation script that verifies versioning logic by creating temporary git repositories with specific tag patterns.
- Expanded `usage.md` and `BEST_PRACTICES.md` with detailed guidance on release tagging patterns, hybrid workspace configurations, and CI/CD validation.
- Reinforced security best practices by ensuring path traversal protection and validating sandboxed Jinja2 rendering.
- Refined the `README.md` and overall documentation for better clarity on tag matching behavior and default patterns.
