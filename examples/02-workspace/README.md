# Workspace Example

This example demonstrates using `uv-workspace-dynamic-versioning` in a monorepo/workspace setup.

## Structure

```
example-workspace/
├── pyproject.toml          # Workspace root
├── packages/
│   ├── pkg-a/
│   │   ├── pyproject.toml
│   │   └── src/pkg_a/__init__.py
│   └── pkg-b/
│       ├── pyproject.toml
│       └── src/pkg_b/__init__.py
```

## Key Configuration

**Root `pyproject.toml`:**
```toml
[tool.uv.workspace]
members = ["packages/*"]
```

**Package `pyproject.toml`:**
```toml
[tool.hatch.version]
source = "uv-workspace-dynamic-versioning"
```

## Usage

```bash
# Build all packages
uv build --all

# Build specific package
cd packages/pkg-a && hatch build
```

## Directory-Specific History

The plugin automatically patches git history for each package's directory, ensuring:
- Version distance reflects commits touching that specific package
- Commit hash reflects the latest change to that package
- Dirty state reflects uncommitted changes in that directory
