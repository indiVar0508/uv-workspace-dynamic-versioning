# Basic hatchling Example

This is the minimal configuration to use `uv-workspace-dynamic-versioning` with hatchling.

## Files

```
example-basic/
├── pyproject.toml    # Package configuration
└── src/
    └── example_basic/
        └── __init__.py
```

## Key Configuration

```toml
[tool.hatch.version]
source = "uv-workspace-dynamic-versioning"
```

This tells hatch to use our plugin as the version source.

## Usage

```bash
# Build the package
hatch build

# Or with uv
uv build
```

## Requirements

- Git repository with at least one tag (e.g., `v0.1.0`)
- hatchling in build dependencies
- uv-workspace-dynamic-versioning in build dependencies
