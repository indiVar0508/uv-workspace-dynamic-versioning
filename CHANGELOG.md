# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2026-03-22

### Fixed
- Added missing license and comprehensive metadata to `pyproject.toml` for better PyPI discoverability.

## [0.1.0] - 2026-03-17

### Added
- Initial release of `uv-workspace-dynamic-versioning`.
- Dynamic version source plugin for `uv` workspaces integrated with `hatch`.
- `DynamicWorkspaceVersionSource` for VCS-based versioning with directory-specific history patching.
- `DependenciesMetadataHook` for dynamic dependency management in workspaces.
- Security hardening for Jinja2 (SandboxedEnvironment) and path traversal protection.
- Automated CI/CD workflow with GitHub Actions and Trusted Publisher (PyPI).
- Comprehensive documentation site using Material for MkDocs.
- High test coverage (74%+) with unit tests for core components.
