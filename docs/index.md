# uv-workspace-dynamic-versioning

<p align="center">
  <img src="https://raw.githubusercontent.com/squidfunk/mkdocs-material/master/src/assets/logo.svg" width="100" />
</p>

<p align="center">
  <em>A powerful Hatch plugin for dynamic versioning and dependency injection in uv workspaces.</em>
</p>

---

## 🚀 Overview

`uv-workspace-dynamic-versioning` simplifies version management in `uv` workspaces (monorepos). It bridges the gap between VCS tags and project-specific versions, ensuring your workspace remains synchronized and secure.

### 📖 Context & Origin

This project was created to address a specific limitation in the existing `uv-dynamic-versioning` plugin when used within complex monorepos and `uv` workspaces.

As discussed in [ninoseki/uv-dynamic-versioning#81](https://github.com/ninoseki/uv-dynamic-versioning/issues/81#issuecomment-3756445422), the standard implementation often calculates version distance and commit hashes based on the **entire repository history**. In a workspace with multiple packages, this leads to:
1.  **False Positives**: Packages bumping versions when unrelated code in the workspace changes.
2.  **Inaccurate Metadata**: Commit hashes reflecting global repo state rather than the state of the specific package.

`uv-workspace-dynamic-versioning` introduces **Directory-Specific Patching**. It re-calculates the Git distance and commit hash by filtering the history to the specific package subdirectory, ensuring that versions only reflect changes relevant to that package.

---

## ✨ Key Features

*   **VCS-Powered Versioning**: Automatically derive versions from Git, Mercurial, and more via [Dunamai](https://github.com/mtkennerly/dunamai).
*   **Workspace Aware**: Accurate `distance` and `commit` hash calculation restricted to the project subdirectory.
*   **Dynamic Dependencies**: Inject versions into `dependencies` using Jinja2 templates (e.g., `pkg == {{ version.base }}`).
*   **Secure by Design**: Sandboxed Jinja2 environment and Path Traversal protection.
*   **Highly Configurable**: Custom formats, bumping logic, and fallback versions.

---

## 🛠 Quick Start

### 1. Installation

Add the plugin to your `build-system.requires` in `pyproject.toml`:

```toml
[build-system]
requires = ["hatchling", "uv-workspace-dynamic-versioning"]
build-backend = "hatchling.build"
```

### 2. Basic Configuration

Enable the version source and mark the version as dynamic:

```toml
[project]
name = "my-awesome-package"
dynamic = ["version"]

[tool.hatch.version]
source = "uv-workspace-dynamic-versioning"
```

---

## 📖 Why Choose This Plugin?

In a monorepo, a single Git tag often applies to multiple packages. Standard versioning tools might report the same version for all packages, regardless of which ones actually changed. 

**This plugin is different.** It patches the version metadata to reflect the history of the **specific package directory**, ensuring that version bumps only happen where they are needed.

---

## 🎓 Next Steps

*   [Follow the Getting Started Guide](usage.md)
*   [Explore Configuration Options](configuration.md)
*   [Check the API Reference](api.md)
