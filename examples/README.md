# Examples

This directory contains minimal examples demonstrating the use of `uv-workspace-dynamic-versioning`.

## Quick Examples

| Example | Description |
|---------|-------------|
| [01-basic-hatchling](./01-basic-hatchling/) | Basic setup with hatchling |
| [02-workspace](./02-workspace/) | Monorepo/workspace setup |
| [03-jinja-templating](./03-jinja-templating/) | Jinja2 template rendering |
| [04-dynamic-dependencies](./04-dynamic-dependencies/) | Dynamic dependency resolution |
| [05-custom-format](./05-custom-format/) | Custom version formats |

## Example 1: Basic hatchling Setup

```toml
# pyproject.toml
[project]
name = "my-package"
dynamic = ["version"]
dependencies = []

[build-system]
requires = ["hatchling", "uv-workspace-dynamic-versioning"]
build-backend = "hatchling.build"

[tool.hatch.version]
source = "uv-workspace-dynamic-versioning"
```

## Example 2: Workspace with Multiple Packages

```toml
# pyproject.toml (root)
[tool.uv.workspace]
members = ["packages/*"]
```

```toml
# packages/my-package/pyproject.toml
[project]
name = "my-package"
dynamic = ["version"]

[build-system]
requires = ["hatchling", "uv-workspace-dynamic-versioning"]
build-backend = "hatchling.build"

[tool.hatch.version]
source = "uv-workspace-dynamic-versioning"
```

## Example 3: Jinja2 Template

```toml
[tool.uv-workspace-dynamic-versioning]
format-jinja = "v{{ major }}.{{ minor }}.{{ patch }}-{{ branch | default('main') }}"
```

## Example 4: Dynamic Dependencies

```toml
[project]
name = "my-package"
dynamic = ["version", "dependencies"]

[tool.hatch.version]
source = "uv-workspace-dynamic-versioning"

[tool.uv-workspace-dynamic-versioning.dependencies]
dependencies = [
    "mypackage=={{ version }}",
    "common~={{ major }}.{{ minor }}"
]
```

---

For more details, see the [main documentation](../README.md).
