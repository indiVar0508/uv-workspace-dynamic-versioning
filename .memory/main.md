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
- Test coverage reached **74%** with unit tests for configuration, versioning, and metadata hooks.
- **v0.1.0** released on PyPI via GitHub Actions with Trusted Publisher (OpenID Connect).
- Metadata in `pyproject.toml` updated for better discoverability and maintainability.

## Key Decisions Made
- **Build Backend:** Using `hatchling`.
- **Versioning Engine:** Using `dunamai`.
- **Documentation UX:** Adopted Material for MkDocs with light/dark mode toggles, code copy buttons, and automated API reference via `mkdocstrings`.
- **Quality Control:** Integrated `pytest-cov` for coverage tracking.
- **Repository Hygiene:** Site artifacts and test caches ignored in `.gitignore`.
- **Commit Strategy:** Adopted [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) for all repository changes to ensure a clear and machine-readable project history.
- **Security Hardening**:
    - Mitigated SSTI by using Jinja2 SandboxedEnvironment.
    - Prevented Path Traversal by validating `from-file.source` against the project root.
    - Improved robustness by logging Git subprocess failures to stderr instead of silencing them.
- **Deployment Strategy**: Using GitHub Actions with Trusted Publishers for secure PyPI releases.

## Milestones
- [x] Project initialization.
- [x] Basic plugin structure and entry points.
- [x] Core versioning logic implementation.
- [ ] Integration testing with `uv` workspaces.
- [x] High-quality Documentation (UX + API).
- [x] 74%+ Test Coverage.
- [x] Security Hardening (SSTI + Path Traversal).
- [x] Initial release (v0.1.0).

## Open Questions
- How to handle the transition to MkDocs 2.0 when it becomes stable?
- Should we add automated release notes generation?
