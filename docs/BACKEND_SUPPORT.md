# Backend Support

This document outlines which build backends are supported by `uv-workspace-dynamic-versioning`.

## Overview

`uv-workspace-dynamic-versioning` is a **hatch plugin**. It registers with hatch's plugin system via entry points:

```toml
[project.entry-points.hatch]
uv-workspace-dynamic-versioning = "uv_workspace_dynamic_versioning.hooks"
```

This means **only backends that use hatch/hatchling** can discover and use the version source.

## Support Matrix

| Backend | Version Source | Metadata Hook | Notes |
|---------|---------------|---------------|-------|
| **hatchling** | ✅ Full Support | ✅ Full Support | Primary backend |
| **hatch** | ✅ Full Support | ✅ Full Support | Uses hatchling internally |
| **uv build** | ✅ Full Support | ✅ Full Support | Uses hatchling internally |
| **pdm-backend** | ❌ Not Supported | ❌ Not Supported | Different plugin system |
| **setuptools** | ⚠️ Bypass Only | ⚠️ Bypass Only | Use `UV_DYNAMIC_VERSIONING_BYPASS` |
| **flit_core** | ⚠️ Bypass Only | ⚠️ Bypass Only | Use `UV_DYNAMIC_VERSIONING_BYPASS` |
| **scikit-build-core** | ⚠️ Bypass Only | ⚠️ Bypass Only | Use `UV_DYNAMIC_VERSIONING_BYPASS` |
| **maturin** | ❌ Not Supported | ❌ Not Supported | Rust-based, different system |
| **meson-python** | ❌ Not Supported | ❌ Not Supported | Different plugin system |
| **build** (pypa) | ⚠️ Via hatchling | ⚠️ Via hatchling | Uses hatchling as backend |

## Detailed Explanation

### ✅ Full Support: hatchling, hatch, uv build

These backends support the full plugin interface:

```toml
[build-system]
requires = ["hatchling", "uv-workspace-dynamic-versioning"]
build-backend = "hatchling.build"

[tool.hatch.version]
source = "uv-workspace-dynamic-versioning"
```

```bash
# All of these work
hatch build
uv build
python -m build  # if hatchling is in requires
```

### ⚠️ Bypass Only: setuptools, flit_core, etc.

For backends without hatch plugin support, use the environment variable bypass:

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
version = "0.0.0"  # Will be overridden by environment variable
```

```bash
# Set version via environment
UV_DYNAMIC_VERSIONING_BYPASS=1.2.3 pip wheel .
```

Or use a pre-build script to generate the version.

### ❌ Not Supported: pdm-backend, maturin, meson-python

These have their own plugin systems incompatible with hatch plugins.

**Alternatives:**
- Switch to hatchling
- Use separate version management scripts

## CI/CD Examples

### GitHub Actions

```yaml
- name: Build with hatchling
  run: |
    hatch build

- name: Build with setuptools fallback
  run: |
    UV_DYNAMIC_VERSIONING_BYPASS=$(hatch version) pip wheel .
```

### GitLab CI

```yaml
build:
  script:
    - pip install uv-workspace-dynamic-versioning
    - hatch build
```

### Local Development

```bash
# Full hatchling support
hatch build
uv build

# With version bypass for testing
UV_DYNAMIC_VERSIONING_BYPASS=1.0.0.dev0 pip wheel .
```

## Why Only hatchling?

The plugin implements hatch's `VersionSourceInterface` and `MetadataHookInterface`. This is a hatch-specific API that other build backends don't implement.

To add support for other backends, you would need:
1. **setuptools**: Implement a `setuptools.config` version hook
2. **PDM**: Implement PDM's metadata hook interface
3. **flit**: Implement flit's version source plugin

PRs welcome for additional backend support!
