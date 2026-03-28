# uv-workspace-dynamic-versioning

A dynamic versioning plugin for `uv` workspaces, built as a `hatch` extension.

## Project Purpose
To simplify and automate version management in `uv` workspaces by providing a dynamic version source that integrates with the `hatch` build backend.

## Current State
- **Refactored Logic**: Migrated configuration management to Pydantic v2 and optimized the versioning engine for accuracy in monorepos.
- **Improved Accuracy**: Fixed directory-specific patching logic to use localized path filters, preventing version "bleeding" between workspace packages.
- **Enhanced Quality**: Reached **92%** test coverage with comprehensive tests for edge cases and error handling.
- **Security Gated CI**: Unified CI/CD pipeline ensures that PyPI releases only happen after passing linting, Bandit security scans, and programmatic build validation.
- **Supply Chain Security**: Integrated `actions/attest-build-provenance` with immutable commit SHA pinning to generate verifiable SLSA build provenance for all release artifacts.
- **Documentation**: Updated with industry best practices for monorepos, release tagging, and hybrid workspace architectures.

## Maintainer Role & Accountability
As the official maintainer of `uv-workspace-dynamic-versioning`, I am responsible for:
1.  **Code Stewardship**: Ensuring the Python implementation follows PEP 8, is type-safe, and utilizes the latest language features (Python 3.10+).
2.  **Package Integrity**: Managing `pyproject.toml` metadata, dependencies, and entry points.
3.  **Security Advocacy**: Enforcing sandboxing for Jinja2, preventing path traversal, and auditing all `subprocess` interactions.
4.  **Release Management**: Curating `CHANGELOG.md`, managing git tags, and supervising the automated release pipeline to PyPI.
6.  **Security First**: Hardening supply chain security by pinning all project and build-system dependencies to exact versions and using immutable commit SHAs for all GitHub Actions to ensure deterministic and verifiable builds.

## Key Decisions Made
- **Build Backend:** Using `hatchling`.
- **Versioning Engine:** Using `dunamai`.
- **Configuration**: Standardized on Pydantic v2 with `validate_default=True` for robust runtime validation.
- **Security**: Enforced Bandit scanning and list-based `subprocess` arguments to eliminate shell injection risks.
- **Security First**: Adopted a project-wide policy of pinning all infrastructure, build-system, and project dependencies to exact versions and immutable commit SHAs, minimizing exposure to upstream dependency drift and compromised releases.
- **CI Architecture**: Adopted a gated single-pipeline strategy where `publish` depends on all validation stages.
- **Hybrid Support**: Formalized support for hybrid workspaces where root projects and members use different dynamic versioning plugins.

## Milestones
- [x] Project initialization.
- [x] Basic plugin structure and entry points.
- [x] Core versioning logic implementation.
- [x] Integration testing with `uv` workspaces.
- [x] High-quality Documentation (UX + API).
- [x] 90%+ Test Coverage.
- [x] Security Hardening (SSTI + Path Traversal + Subprocess Audit).
- [x] Automated Release Gating (CI/CD).
- [x] Initial release (v0.1.0).
- [x] Stable Pydantic v2 Refactor (v0.1.3).
- [x] Integrated SLSA Build Provenance (v4.1.0).

## Open Questions
- How to handle the transition to MkDocs 2.0 when it becomes stable?
- Should we add automated release notes generation?
