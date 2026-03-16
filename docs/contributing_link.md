# Contributing

We love contributions! Please check out our [Contributing Guidelines](https://github.com/indiVar0508/uv-workspace-dynamic-versioning/blob/main/CONTRIBUTING.md) on GitHub.

## Development Setup

1.  **Clone the Repo**:
    ```bash
    git clone https://github.com/indiVar0508/uv-workspace-dynamic-versioning
    ```

2.  **Install Dependencies**:
    ```bash
    uv sync --all-extras
    ```

3.  **Run Tests**:
    ```bash
    PYTHONPATH=src pytest --cov=src
    ```

4.  **Build Documentation**:
    ```bash
    mkdocs serve
    ```
