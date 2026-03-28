# Dynamic Dependencies Example

This example demonstrates using the metadata hook to resolve dependencies with version templating.

## Key Configuration

```toml
[project]
dynamic = ["version", "dependencies"]
```

```toml
[tool.hatch.metadata.hooks.uv-workspace-dynamic-versioning]

[tool.uv-workspace-dynamic-versioning.dependencies]
dependencies = [
    "requests>={{ major }}.{{ minor }}.0",
]
optional-dependencies.dev = [
    "pytest=={{ major }}.{{ minor }}.0",
]
```

## Available Template Variables

Same as Jinja2 templating - you can use `{{ version }}`, `{{ major }}`, etc.

## How It Works

1. The metadata hook runs after version detection
2. Templates are rendered with the detected version
3. Dependencies are injected into the built metadata

## Usage

```bash
# Build and check dependencies
hatch build
pip show example-deps

# With optional dependencies
pip install example-deps[dev]
```

## Requirements

- `dependencies` and/or `optional-dependencies` must be listed in `project.dynamic`
