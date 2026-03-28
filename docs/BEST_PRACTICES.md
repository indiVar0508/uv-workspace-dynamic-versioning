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

### Version Bumping

The plugin auto-bumps based on configuration:

```toml
[tool.uv-workspace-dynamic-versioning]
bump = true  # Smart bumping
```

Or use Jinja templates for custom bumping:

```toml
[tool.uv-workspace-dynamic-versioning]
format-jinja = "{{ major }}.{{ minor }}.{{ patch }}"
```

### Release Process

1. **Development:**
   ```bash
   # Work on features...
   git commit -m "feat: add new feature"
   ```

2. **Tag Release:**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

3. **Build:**
   ```bash
   hatch build
   # or
   uv build
   ```

### Hotfix Process

```bash
# From tag
git checkout v1.0.0
git checkout -b hotfix/v1.0.1

# Fix and commit
git commit -m "fix: critical bug"

# Tag and build
git tag v1.0.1
hatch build
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Build and Test

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for versioning

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install
        run: pip install hatch hatch-vcs uv-workspace-dynamic-versioning

      - name: Build
        run: hatch build

      - name: Test
        run: hatch run pytest
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
