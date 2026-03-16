# main

**Purpose:** Main project memory branch

---

## Commit 59cd4601 | 2026-03-16T22:18:18.615Z

### Branch Purpose
The `main` branch serves as the primary project memory for the development of `uv-workspace-dynamic-versioning`, a plugin designed to automate version management in `uv` workspaces.

### Previous Progress Summary
Initial commit.

### This Commit's Contribution
- Established the initial project roadmap and memory structure for a `hatch` extension facilitating dynamic versioning in `uv` workspaces.
- Selected `hatchling` as the build backend and `dunamai` as the core engine for generating versions based on VCS state.
- Integrated `tomlkit` for robust `pyproject.toml` manipulation and `jinja2` for potential version string templating.
- Configured plugin entry points to register the `uv-workspace-dynamic-versioning` extension as a `hatch` hook.
- Established the basic project structure and core logic modules, including a vendored subdirectory for specialized requirements.

---

## Commit 6eaed424 | 2026-03-16T22:19:00.525Z

### Branch Purpose
The `main` branch serves as the primary project memory for the development of `uv-workspace-dynamic-versioning`, a plugin designed to automate version management in `uv` workspaces.

### Previous Progress Summary
The project was initialized with a roadmap and memory structure for a `hatch` extension providing dynamic versioning in `uv` workspaces. `hatchling` was selected as the build backend, `dunamai` as the versioning engine, and `tomlkit`/`jinja2` for configuration and templating. Initial work established the project structure, registered plugin entry points, and populated core logic, much of which resides in a `vendored` subdirectory.

### This Commit's Contribution
- Refined the project's current state and key decisions following a detailed code review of the existing `hatch` plugin implementation.
- Identified that the plugin provides both a `DynamicWorkspaceVersionSource` for VCS-based versioning and a `DependenciesMetadataHook` for dynamic dependency updates via Jinja2 templates.
- Confirmed the implementation of directory-specific git history patching to calculate accurate version distance within monorepos/workspaces.
- Validated the use of `tomlkit` for programmatic `pyproject.toml` manipulation and `jinja2` for both version string and dependency list templating.

---

## Commit 980fcf72 | 2026-03-16T22:20:12.617Z

### Branch Purpose
The `main` branch serves as the primary project memory for the development of `uv-workspace-dynamic-versioning`, a plugin designed to automate version management in `uv` workspaces.

### Previous Progress Summary
The project was established as a `hatch` extension for `uv` workspaces, utilizing `hatchling` as the build backend and `dunamai` for VCS-based versioning. Initial work defined the project structure and registered core plugin entry points, including a `DynamicWorkspaceVersionSource` for directory-specific git history patching and a `DependenciesMetadataHook` for dynamic dependency updates via Jinja2 templates. A subsequent code review validated the implementation's use of `tomlkit` for configuration manipulation and `jinja2` for version and dependency templating, confirming the project's ability to handle complex monorepo versioning requirements.

### This Commit's Contribution
- Created a comprehensive MkDocs documentation suite to provide clear guidance for users and developers.
- Drafted the project overview and installation guides, highlighting the plugin's utility in `uv` monorepo environments.
- Documented usage patterns for basic setup, workspace-aware versioning, and dynamic dependency injection.
- Provided a detailed configuration reference for all version source and metadata hook options, including Jinja2 context details.
- Outlined the internal API for core components to assist with future development and maintenance.
- Configured the MkDocs build using the Material theme and established a structured navigation menu in `mkdocs.yml`.

---

## Commit 1a0f8284 | 2026-03-16T22:20:27.637Z

### Branch Purpose

The `main` branch serves as the primary project memory for the development of `uv-workspace-dynamic-versioning`, a plugin designed to automate version management in `uv` workspaces.

### Previous Progress Summary

The project was established as a `hatch` extension for `uv` workspaces, utilizing `hatchling` as the build backend and `dunamai` for VCS-based versioning. Initial work defined the project structure and registered core plugin entry points, including a `DynamicWorkspaceVersionSource` for directory-specific git history patching and a `DependenciesMetadataHook` for dynamic dependency updates via Jinja2 templates. Subsequent code reviews and implementation work validated the use of `tomlkit` for configuration manipulation and `jinja2` for version and dependency templating, confirming the project's ability to handle complex monorepo versioning requirements. Most recently, a comprehensive MkDocs documentation suite was created, providing clear guidance for users and developers on installation, usage, and configuration.

### This Commit's Contribution

- Updated the project roadmap milestones in `.memory/main.md` to accurately reflect the current development status.
- Formally marked the core versioning logic implementation and project documentation as completed.
- Refined the roadmap to highlight integration testing with `uv` workspaces as the primary remaining objective for the current phase.

---

## Commit 59709875 | 2026-03-16T22:28:43.405Z

### Branch Purpose
The `main` branch serves as the primary project memory for the development of `uv-workspace-dynamic-versioning`, a plugin designed to automate version management in `uv` workspaces.

### Previous Progress Summary
The project was established as a `hatch` extension for `uv` workspaces, using `hatchling` as the build backend and `dunamai` for VCS-based versioning. Key features include directory-specific git history patching and dynamic dependency updates via Jinja2 templates, with `tomlkit` handling `pyproject.toml` manipulation. A comprehensive MkDocs documentation suite was completed, providing guides for installation, usage, and configuration. The roadmap was refined to mark core logic and documentation as complete, shifting focus toward integration testing and community readiness.

### This Commit's Contribution
- Formalized the development environment by adding `docs` and `test` optional dependencies to `pyproject.toml`.
- Established `CONTRIBUTING.md` with standards for bug reporting, `uv`-based setup, and documentation best practices.
- Implemented a `pytest` suite covering schema validation, metadata hook configuration, and directory-specific version patching logic.
- Validated core versioning logic through successful test execution, including mocked `subprocess` calls for git history distance calculation.
- Confirmed documentation build stability by verifying a successful `mkdocs build` against the established site structure.

---

## Commit 7bd205a6 | 2026-03-16T22:35:33.423Z

### Branch Purpose

The `main` branch serves as the primary project memory for the development of `uv-workspace-dynamic-versioning`, a plugin designed to automate version management in `uv` workspaces.

### Previous Progress Summary

The project was established as a `hatch` extension for `uv` workspaces, using `hatchling` as the build backend and `dunamai` for VCS-based versioning. Key features include directory-specific git history patching and dynamic dependency updates via Jinja2 templates. A comprehensive MkDocs documentation suite, contribution guidelines, and a `pytest` suite were established to ensure project quality and community readiness. The project structure and core logic modules, including a vendored subdirectory, are formalized with development dependencies and validated through initial testing.

### This Commit's Contribution

- Integrated `mkdocstrings` into the documentation workflow to automate API reference generation from source code docstrings.
- Enriched core modules (`version_source.py`, `main.py`, `metadata_hook.py`) with comprehensive docstrings to facilitate maintenance and automated documentation.
- Enhanced repository hygiene by adding build artifacts (`site/`) and testing caches (`.pytest_cache/`) to `.gitignore`.
- Updated the documentation site layout and `mkdocs.yml` to include Material theme features like code copy buttons and navigation indexes.
- Acknowledged MkDocs 2.0 compatibility considerations in the project roadmap while maintaining 1.x stability for current production use.

---

## Commit 25a8b84e | 2026-03-16T22:38:58.681Z

### Branch Purpose

The `main` branch serves as the primary project memory for the development of `uv-workspace-dynamic-versioning`, a `hatch` plugin designed to automate version management and dependency injection in `uv` workspaces.

### Previous Progress Summary

The project was established as a `hatch` extension using `hatchling` and `dunamai` for VCS-based versioning, featuring custom directory-specific history patching to support accurate versioning within monorepos. It enables dynamic dependency updates via Jinja2 templates and `tomlkit` for robust configuration manipulation. A comprehensive foundation was built with an MkDocs Material documentation suite, contribution guidelines, and a `pytest` suite. Recent iterations formalized the development environment, automated API reference generation via `mkdocstrings` with enriched source docstrings, and established repository hygiene by standardizing build and cache exclusions in `.gitignore`.

### This Commit's Contribution

- Achieved **71% test coverage** by expanding the test suite to validate configuration parsing, metadata hook rendering, and mocked git history distance calculations.
- Significantly enhanced documentation UX by implementing **light/dark mode toggles**, search suggestions, TOC tracking, and improved navigation features.
- Integrated `mkdocs-minify-plugin` and `mkdocs-git-revision-date-localized-plugin` to optimize documentation builds and provide automated "last updated" metadata.
- Standardized the development environment by adding `pytest-cov` and specialized MkDocs plugins to the project's optional dependencies.
- Updated the project roadmap to reflect the completion of the 70%+ test coverage milestone and the delivery of high-quality documentation.

---

## Commit fd32768f | 2026-03-16T22:48:29.933Z

### Branch Purpose

The `main` branch serves as the primary project memory for the development of `uv-workspace-dynamic-versioning`, a `hatch` plugin designed to automate version management and dependency injection in `uv` workspaces.

### Previous Progress Summary

The project was established as a `hatch` extension using `hatchling` and `dunamai` for VCS-based versioning, featuring custom directory-specific history patching for monorepos. It enables dynamic dependency updates via Jinja2 templates and `tomlkit` for configuration manipulation. A robust foundation includes an MkDocs Material documentation suite with light/dark mode and automated API references, a `pytest` suite reaching 71% coverage, and formalized development standards and repository hygiene.

### This Commit's Contribution

- Mitigated Server-Side Template Injection (SSTI) and arbitrary code execution risks by switching to `jinja2.sandbox.SandboxedEnvironment` for all template rendering.
- Reduced data exposure risks by removing `os.environ` from the default Jinja2 context, preventing accidental leakage of sensitive environment variables in build logs or metadata.
- Hardened dependency security by pinning the minimum `jinja2` version to `3.1.5` to address known vulnerabilities (e.g., CVE-2024-34064).
- Recognized that build-time plugins are a significant supply-chain attack vector, necessitating a "secure by default" posture for user-provided templates.
- Validated that security hardening did not regress core functionality by verifying the existing test suite with the new sandboxed environment.
