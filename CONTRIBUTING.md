# Contributing to uv-workspace-dynamic-versioning

First off, thank you for considering contributing to `uv-workspace-dynamic-versioning`! It's people like you that make the open-source community such a great place to learn, inspire, and create.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct (be kind, be professional).

## How Can I Contribute?

### Reporting Bugs

- **Search for existing issues.**
- **Use a clear and descriptive title.**
- **Describe the exact steps which reproduce the problem.**
- **Include your environment details** (OS, Python version, `uv` version, `hatch` version).

### Suggesting Enhancements

- **Check if the feature has already been suggested.**
- **Explain why this enhancement would be useful.**

### Pull Requests

1. **Fork the repo** and create your branch from `main`.
2. **Install dependencies** using `uv sync --all-extras`.
3. **If you've added code that should be tested, add tests.**
4. **If you've changed APIs, update the documentation.**
5. **Ensure the test suite passes.**
6. **Make sure your code lints.**

## Development Setup

We use `uv` for dependency management.

```bash
# Clone the repository
git clone https://github.com/indiVar0508/uv-workspace-dynamic-versioning
cd uv-workspace-dynamic-versioning

# Create a virtual environment and install dependencies
uv sync --all-extras
```

## Documentation Best Practices

- **Clarity first:** Use simple language.
- **Provide examples:** Every configuration option should have an accompanying snippet.
- **Maintain the structure:** Follow the existing MkDocs layout.
- **Check links:** Ensure all cross-references work.

## Coding Standards

- Follow PEP 8.
- Use type hints for all function signatures.
- Write descriptive docstrings (Google or ReST style).
- Keep functions small and focused.
