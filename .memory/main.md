# uv-workspace-dynamic-versioning

A dynamic versioning plugin for `uv` workspaces, built as a `hatch` extension.

## Project Purpose
To simplify and automate version management in `uv` workspaces by providing a dynamic version source that integrates with the `hatch` build backend.

## Current State
- **Streamlined Architecture**: Removed heavy dependencies (`pydantic`, `tomlkit`) in favor of standard library `dataclasses` and `tomllib` (with `tomli` fallback). This ensures "zero-conflict" for downstream users.
- **Improved Accuracy**: Fixed directory-specific patching logic to use localized path filters, preventing version "bleeding" between workspace packages.
- **Enhanced Quality**: Maintained **92%** test coverage after refactor, with updated tests for the new dataclass-based schema system.
- **Security Gated CI**: Unified CI/CD pipeline ensures that PyPI releases only happen after passing linting, Bandit security scans, and programmatic build validation.
- **v0.1.5 Status**: Refactored to minimize dependency footprint and loosen version constraints. Prepared for release.
- **Security Protocols**: Updated maintainer protocols to ensure zero-automated-tagging. All releases must be initiated by the user.

## Maintainer Role & Accountability
As the official maintainer of `uv-workspace-dynamic-versioning`, I am responsible for:
1.  **Code Stewardship**: Ensuring the Python implementation follows PEP 8, is type-safe, and utilizes the latest language features (Python 3.10+).
2.  **Package Integrity**: Managing `pyproject.toml` metadata, dependencies, and entry points.
3.  **Security Advocacy**: Enforcing sandboxing for Jinja2, preventing path traversal, and auditing all `subprocess` interactions.
4.  **Release Preparation**: Curating `CHANGELOG.md` and preparing metadata for releases. **I am STRICTLY FORBIDDEN from creating Git tags or pushing tags to remote branches.**
5.  **Branch Management**: I may push to feature branches or `main` (if instructed), but **ALWAYS MUST ask for permission before any remote push.**
6.  **Dependency Best Practices**: Minimizing the plugin's footprint by favoring the standard library and using flexible version ranges for remaining dependencies to prevent downstream conflicts.

## Key Decisions Made
- **Build Backend:** Using `hatchling`.
- **Versioning Engine:** Using `dunamai`.
- **Minimal Dependencies**: Replaced Pydantic and `tomlkit` with standard library `dataclasses` and `tomllib` to avoid version conflicts in user environments.
- **Security**: Enforced Bandit scanning and list-based `subprocess` arguments to eliminate shell injection risks.
- **Flexible Versioning**: Adopted flexible version ranges (`>=`) for all project dependencies to improve interoperability.
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
- [x] Streamlined dependency refactor (v0.1.5).

## Open Questions
- How to handle the transition to MkDocs 2.0 when it becomes stable?
- Should we add automated release notes generation?
