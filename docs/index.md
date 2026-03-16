# uv-workspace-dynamic-versioning

A dynamic versioning plugin for `uv` workspaces, built as a `hatch` extension.

## Overview

`uv-workspace-dynamic-versioning` is designed to simplify and automate version management in `uv` workspaces (monorepos). It integrates with the `hatch` build backend to provide:

1.  **VCS-based Dynamic Versioning**: Automatically generates project versions based on Git tags and history.
2.  **Workspace Awareness**: Specifically handles sub-projects within a workspace by calculating version distance based on changes within the sub-project directory.
3.  **Dynamic Dependency Injection**: Allows injecting the current version into `project.dependencies` and `project.optional-dependencies` using Jinja2 templates.

### Why it exists?

In a monorepo managed by `uv`, different packages often need to stay in sync or reference each other's versions dynamically. Managing these versions manually in `pyproject.toml` is error-prone. This plugin automates the process, ensuring that each package has a version reflecting its actual history and that dependencies are correctly updated during the build process.

## Installation

```bash
uv pip install uv-workspace-dynamic-versioning
```

Or add it to your `pyproject.toml` build system requirements:

```toml
[build-system]
requires = ["hatchling", "uv-workspace-dynamic-versioning"]
build-backend = "hatchling.build"
```
