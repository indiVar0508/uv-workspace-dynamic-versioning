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

---

## Commit edf1fd6d | 2026-03-28T18:01:45.907Z

### Branch Purpose

Refactor the codebase for robust configuration validation with Pydantic v2, enhance VCS-based versioning for complex workspaces, and establish a high-standard CI/CD and testing foundation.

### Previous Progress Summary

The branch was established to migrate configuration management to Pydantic v2 and restructure the project into modular components, introducing safe Jinja2 template rendering and modernizing the codebase for Python 3.9+. Early milestones included creating five comprehensive examples and fixing bugs in directory-specific commit history patching and version serialization. Subsequent work added a sixth hybrid workspace example, a build validation script, and extensive documentation on release tagging and CI/CD best practices, ensuring compatibility with both `hatch` and `uv` build backends across single projects and monorepos.

### This Commit's Contribution

- Integrated automated security scanning into the CI pipeline using Bandit and verified sandboxed Jinja2 execution for all template rendering.
- Achieved **74% test coverage** by implementing comprehensive test suites for VCS integration (tag detection, distance calculation) and metadata hook functionality.
- Modernized the codebase with Python 3.10+ union types (`X | Y`) and standardized imports using `ruff` and `isort`.
- Hardened safe `subprocess` calls in `version_source.py` with `# nosec` annotations after verifying list-based argument security.
- Refined the `DependenciesMetadataHook` to support dynamic version injection into both standard and optional dependencies.
- Updated the GitHub Actions workflow (`ci.yml`) to include dedicated jobs for security scanning and independent build validation.
- Fixed a path scoping issue in `git rev-list` to ensure directory-aware versioning remains accurate when executed from subdirectories.

---

## Commit 4933fce7 | 2026-03-28T18:39:37.535Z

### Branch Purpose

Refactor the codebase for robust configuration validation with Pydantic v2, enhance VCS-based versioning for complex workspaces, and establish a high-standard CI/CD and testing foundation.

### Previous Progress Summary

The branch was established to migrate configuration management to Pydantic v2 and restructure the project into modular components, introducing safe Jinja2 template rendering and modernizing the codebase for Python 3.10+. It achieved 74% test coverage and integrated automated security scanning (Bandit) into the CI pipeline. Key technical milestones included optimizing directory-specific history patching, hardening subprocess calls with security annotations, and creating comprehensive examples for hybrid workspace architectures. Compatibility with both `hatch` and `uv` build backends was verified across single projects and monorepos.

### This Commit's Contribution

- Established formal maintainer accountability and updated project documentation to reflect a refined release strategy and professionalized maintenance standards.
- Increased test coverage to **92%** by implementing exhaustive tests for schema edge cases, template rendering variations, and VCS fallback mechanisms.
- Unified the CI/CD pipeline by merging publishing workflows into the main CI suite, enforcing that releases only occur after passing linting, security scans, and functional validation.
- Fixed a critical `KeyError: 'any'` by enabling `validate_default=True` in Pydantic models to ensure Enum normalization for default values.
- Improved the build validation suite by adopting `tomlkit` for programmatic TOML generation, resolving character escaping issues in regex patterns.
- Hardened the repository by cleansing build/test artifacts (`.coverage`, `__pycache__`) from tracking and synchronizing example workspace lockfiles.
- Managed the transition to `v0.1.3` for the next functional release, accommodating PyPI’s immutable artifact policy following initial deployment attempts.

---

## Commit a0aa1986 | 2026-03-28T18:44:45.525Z

### Branch Purpose

Refactor the codebase for robust configuration validation with Pydantic v2, enhance VCS-based versioning for complex workspaces, and establish a high-standard CI/CD and testing foundation.

### Previous Progress Summary

The branch transitioned the project to Pydantic v2 for robust schema validation and restructured the codebase into modular components, introducing safe Jinja2 template rendering and 3.10+ type hinting. It achieved 92% test coverage, integrated Bandit security scanning, and established a unified CI/CD pipeline for gated PyPI releases. Key technical milestones included optimizing directory-specific history patching, fixing PEP 440 regex patterns, and creating comprehensive examples for hybrid workspace architectures. Formal maintainer accountability was established, and documentation was expanded to include industry best practices for monorepo release management.

### This Commit's Contribution

- Hardened supply chain security by pinning GitHub Actions to immutable commit SHAs in the CI/CD pipeline to mitigate risks from tag-based dependency drifting.
- Transitioned from version ranges to specific version pins for build-system and project dependencies in `pyproject.toml` to ensure deterministic builds.
- Codified a "Security First" maintainer policy in project memory, explicitly committing to SHA-pinning for all infrastructure components as a project standard.
- Resolved linting regressions in the coverage test suite to ensure CI checks remain green across all codebase segments.
- Synchronized internal project memory and documentation to reflect the finalized, security-hardened state of the `v0.1.3` release candidate.
