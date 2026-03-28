# uv-workspace-dynamic-versioning

<p align="center">
  <a href="https://pypi.org/project/uv-workspace-dynamic-versioning/">
    <img src="https://img.shields.io/pypi/v/uv-workspace-dynamic-versioning.svg" alt="PyPI version">
  </a>
  <a href="https://github.com/indiVar0508/uv-workspace-dynamic-versioning/actions/workflows/ci.yml">
    <img src="https://github.com/indiVar0508/uv-workspace-dynamic-versioning/actions/workflows/ci.yml/badge.svg" alt="CI Status">
  </a>
  <a href="https://github.com/indiVar0508/uv-workspace-dynamic-versioning">
    <img src="https://img.shields.io/badge/coverage-92%25-brightgreen" alt="Coverage">
  </a>
  <a href="https://github.com/indiVar0508/uv-workspace-dynamic-versioning/attestations">
    <img src="https://img.shields.io/badge/SLSA-Level%203-blue" alt="SLSA Level 3">
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/pypi/l/uv-workspace-dynamic-versioning.svg" alt="License">
  </a>
</p>

<p align="center">
  <em>A powerful Hatch plugin for dynamic versioning and dependency injection in uv workspaces.</em>
</p>

---

## 📖 Context & Origin

This project was created to address a specific limitation in the existing `uv-dynamic-versioning` plugin when used within complex monorepos and `uv` workspaces.

As discussed in [ninoseki/uv-dynamic-versioning#81](https://github.com/ninoseki/uv-dynamic-versioning/issues/81#issuecomment-3756445422), the standard implementation often calculates version distance and commit hashes based on the **entire repository history**. In a workspace with multiple packages, this leads to:
1.  **False Positives**: Packages bumping versions when unrelated code in the workspace changes.
2.  **Inaccurate Metadata**: Commit hashes reflecting global repo state rather than the state of the specific package.

`uv-workspace-dynamic-versioning` introduces **Directory-Specific Patching**. It re-calculates the Git distance and commit hash by filtering the history to the specific package subdirectory, ensuring that versions only reflect changes relevant to that package.

---

## 🚀 Key Features

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

## 📚 Documentation

For full guides and API reference, visit our [Documentation Site](https://github.com/indiVar0508/uv-workspace-dynamic-versioning).

---

## ⚖️ License

Distributed under the terms of the MIT license.
