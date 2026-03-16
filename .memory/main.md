# uv-workspace-dynamic-versioning

A dynamic versioning plugin for `uv` workspaces, built as a `hatch` extension.

## Project Purpose
To simplify and automate version management in `uv` workspaces by providing a dynamic version source that integrates with the `hatch` build backend.

## Current State
- Initial project structure established.
- `hatch` entry points configured for `version_source` and `metadata_hook`.
- Implementation provides `DynamicWorkspaceVersionSource` and `DependenciesMetadataHook`.
- Core logic handles VCS-based versioning with directory-specific git history patching.
- Enhanced documentation with `mkdocs-material`, `mkdocstrings`, and high-quality docstrings.
- Test coverage reached **71%** with unit tests for configuration, versioning, and metadata hooks.

## Key Decisions Made
- **Build Backend:** Using `hatchling`.
- **Versioning Engine:** Using `dunamai`.
- **Documentation UX:** Adopted Material for MkDocs with light/dark mode toggles, code copy buttons, and automated API reference via `mkdocstrings`.
- **Quality Control:** Integrated `pytest-cov` for coverage tracking.
- **Repository Hygiene:** Site artifacts and test caches ignored in `.gitignore`.

## Milestones
- [x] Project initialization.
- [x] Basic plugin structure and entry points.
- [x] Core versioning logic implementation.
- [ ] Integration testing with `uv` workspaces.
- [x] High-quality Documentation (UX + API).
- [x] 70%+ Test Coverage.

## Open Questions
- How to handle the transition to MkDocs 2.0 when it becomes stable?
- Should we add automated CI (GitHub Actions) for running tests and building docs?
