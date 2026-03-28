# Hybrid Workspace Example

This example demonstrates how to use `uv-dynamic-versioning` at the workspace root and `uv-workspace-dynamic-versioning` for individual workspace members.

## Architecture

- **Root project**: Uses `uv-dynamic-versioning`. It tracks the overall project version based on any commit in the repository.
- **`pkg-a`**: Uses `uv-workspace-dynamic-versioning`. Its version only reflects changes within `packages/pkg-a`.
- **`pkg-b`**: Uses `uv-workspace-dynamic-versioning`. Its version only reflects changes within `packages/pkg-b`.

## How it works

1. When you commit a change at the root (not in any package), only the root project's version will advance.
2. When you commit a change in `packages/pkg-a`, both the root project and `pkg-a` versions will advance, but `pkg-b` will remain at its current version.
3. When you tag a release (e.g., `v1.0.0`), all projects will align to that version.

## Try it out

Install the tools:
```bash
pip install hatch uv-dynamic-versioning uv-workspace-dynamic-versioning
```

Check versions:
```bash
# In the root
hatch version

# In pkg-a
cd packages/pkg-a && hatch version

# In pkg-b
cd packages/pkg-b && hatch version
```
