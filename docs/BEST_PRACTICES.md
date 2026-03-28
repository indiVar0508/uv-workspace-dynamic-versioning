# Best Practices

This document outlines best practices for maintaining a Python project using `uv-workspace-dynamic-versioning`.

## Project Structure

### Recommended Layout

```
my-project/
├── pyproject.toml           # Root workspace config (optional)
├── packages/
│   ├── package-a/
│   │   ├── pyproject.toml
│   │   └── src/
│   │       └── package_a/
│   │           └── __init__.py
│   └── package-b/
│       └── ...
├── examples/                # Example usage
├── tests/                   # Project tests
└── docs/                    # Documentation
```

### Minimal Package Structure

```
my-package/
├── pyproject.toml
└── src/
    └── my_package/
        ├── __init__.py
        └── __main__.py
```

## Git Configuration

### Tag Format

Use semantic version tags:

```bash
git tag v1.0.0
git tag v1.2.3
git tag v2.0.0-rc1
```

### Recommended .gitignore

```gitignore
# Build outputs
dist/
build/
*.egg-info/

# Python
__pycache__/
*.py[cod]
.venv/
.eggs/

# Testing
.pytest_cache/
.coverage
htmlcov/

# IDE
.idea/
.vscode/
*.swp
```

### Branch Naming

Use descriptive branch names:

```bash
git checkout -b feature/dynamic-dependencies
git checkout -b fix/version-parsing
git checkout -b release/v1.2.0
```

## Version Management

### Release Tagging Patterns

For most Python projects, it is standard to use "clean" version tags (e.g., `v1.2.3`). 
The `dunamai` engine automatically handles the generation of development and post-release versions (like `1.2.3.post1.dev0+g<hash>`) for your artifacts based on the distance from the last tag.

- **Clean tags:** Use `v1.2.3`. Avoid `.dev` or `.post` in the tags themselves unless it's a pre-release like `v1.2.3-rc1`.
- **Pre-releases:** Use `v1.2.3-rc1`. `dunamai` will recognize this as a stage.
- **Build artifacts:** Let the plugin handle the `.post` and `.dev` suffixes for non-tagged commits.

### Hybrid Workspace Setup (Root + Members)

A common pattern for monorepos is to have:
1.  **Root package:** Tracks the overall project's version and is tagged with `vX.Y.Z`.
2.  **Workspace members:** Depend on the root package but may have their own versioning.

If you use `uv-dynamic-versioning` at the root and `uv-workspace-dynamic-versioning` for members:
- The root version will reflect the distance from the last tag based on *any* commit in the repository.
- Each member's version will reflect the distance from the last tag based *only* on commits within that member's directory.

This allows you to release a new version of the root package while keeping individual member versions stable if they haven't changed.

### Bumping Strategies

If you want the version to ALWAYS be "ahead" of the last tag, use `bump = true`:

```toml
[tool.uv-workspace-dynamic-versioning]
bump = true
```

If the last tag was `v1.0.0` and there are 2 commits in the directory, the version will be `1.0.1.post2.dev0+...` instead of `1.0.0.post2.dev0+...`.

## CI/CD Validation

### Automated Version Checks

When releasing your `.whl` files, it is recommended to validate that the version was generated correctly. You can automate this by:
1.  Checking the built artifact's filename or metadata.
2.  Running a "bootstrap" script that builds a test repo using your plugin.

See [scripts/validate_build.py](../scripts/validate_build.py) for a reference implementation.

### GitHub Actions Workflow

Ensure you fetch the full git history for correct versioning:

```yaml
steps:
  - uses: actions/checkout@v4
    with:
      fetch-depth: 0  # CRITICAL for dynamic versioning
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
      - id: ruff-format
```

## Testing

### Test the Version Source

```python
# tests/test_version.py
import pytest
from pathlib import Path

from uv_workspace_dynamic_versioning.version_source import get_version
from uv_workspace_dynamic_versioning.schemas import PluginConfig


def test_version_detection():
    config = PluginConfig()
    version, _ = get_version(config, Path("."))
    assert version  # Version should be non-empty
```

### Test with Fixtures

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
```

## Documentation

### Docstrings

```python
"""Short summary.

Longer description if needed.

Args:
    param1: Description of param1
    param2: Description of param2

Returns:
        Description of return value

Raises:
    ValueError: When this happens
"""
```

### README Structure

```markdown
# Project Name

Brief description.

## Installation

pip install project-name

## Usage

Basic usage example.

## Configuration

See [docs/CONFIGURATION.md](docs/CONFIGURATION.md)

## License

MIT
```

## Security

### Version File Security

The plugin prevents path traversal:

```toml
# This is SAFE - file is within project
[tool.uv-workspace-dynamic-versioning]
from-file.source = "VERSION"

# This will FAIL - file is outside project
[tool.uv-workspace-dynamic-versioning]
from-file.source = "../../secrets/version"
```

### Jinja Sandbox

Templates are rendered in a sandboxed environment to prevent code execution.

## Performance

### Caching

The version is computed once per build. For large workspaces, consider:

```toml
[tool.uv-workspace-dynamic-versioning]
fallback-version = "0.0.0"
```

### Large Repositories

For repositories with many commits, use `latest-tag`:

```toml
[tool.uv-workspace-dynamic-versioning]
latest-tag = true  # Only look at commits since latest tag
```

## Troubleshooting

### No Tags Found

```bash
# Create initial tag
git tag v0.0.1
git push origin v0.0.1
```

### Dirty Working Directory

```bash
# Commit or stash changes
git add .
git commit -m "work in progress"
```

Or use the bypass:

```bash
UV_DYNAMIC_VERSIONING_BYPASS=1.0.0 hatch build
```

### Permission Denied (Git)

```bash
# Ensure git can find your remote
git remote -v
git fetch origin
```
