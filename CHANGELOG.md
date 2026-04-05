# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.4] - 2026-04-05

### Added
- Native support for building in Docker/missing-VCS environments via workspace version inheritance.
- Poetry-style version overrides via `UV_WORKSPACE_DYNAMIC_VERSIONING_OVERRIDE` (package-specific) and `UV_WORKSPACE_DYNAMIC_VERSIONING_BYPASS` (global).
- Integrated SLSA Level 3 build provenance with secure build attestations.
- CI Hardening: Pinning all tools (`uv`, `bandit`) and actions to immutable commit SHAs on Node 24.

### Fixed
- Resolved CI security scan failures by properly syncing dev dependencies for `bandit`.
- Suppressed `try-except-pass` warnings where broad exception handling is intentional for configuration fallbacks.
- Corrected version discrepancy in example workspace dependencies.

## [0.1.3] - 2026-03-28

### Added
- Comprehensive test suite in `tests/test_full_coverage.py`, increasing coverage to **92%**.
- Automated security scanning with Bandit in the CI pipeline.
- Programmatic build validation script `scripts/validate_build.py` for CI safety.
- Hybrid workspace example in `examples/06-hybrid-workspace` demonstrating `uv-dynamic-versioning` + `uv-workspace-dynamic-versioning`.

### Fixed
- Fixed CI/CD workflow trigger to properly publish on git tags.
- Hardened supply chain security by pinning GitHub Action SHAs to immutable commit SHAs.
- Fixed critical `KeyError: 'any'` caused by un-normalized default values in Pydantic schemas.
- Fixed `TOMLDecodeError` in build scripts by properly escaping regex backslashes in generated TOML.
- Fixed directory-specific Git history patching to use correct relative path filters.
- Fixed test failures resulting from strict Enum normalization.
- Corrected `.gitignore` to properly exclude all Python cache files (`__pycache__`, `.pyc`).

### Changed
- Unified CI/CD workflow: Publishing to PyPI now requires successful completion of linting, security scans, and build validation.
- Modernized type annotations across the codebase to use Python 3.10+ `|` syntax.
- Updated documentation with industry best practices for release management and monorepo architectures.

## [0.1.2] - 2026-03-28 [YANKED]

### Added
- Initial Pydantic v2 migration.
- Basic hybrid workspace example.

### Fixed
- Improved directory-specific patching logic.

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
