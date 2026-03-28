# Custom Format Examples

This example demonstrates different version format styles.

## Supported Styles

### PEP 440 (default for Python)

```toml
[tool.uv-workspace-dynamic-versioning]
style = "pep440"
```

Examples: `1.0.0`, `1.2.3a1`, `2.0.0rc1`, `1.0.0.post1`

### Semantic Versioning

```toml
[tool.uv-workspace-dynamic-versioning]
style = "semver"
```

Examples: `1.0.0`, `1.2.3-alpha`, `2.0.0-rc.1`

### PVP (Haskell-style)

```toml
[tool.uv-workspace-dynamic-versioning]
style = "pvp"
```

Examples: `1.0`, `1.2.3-tag`, `2.0-beta`

## Version Format String

Use the `format` option for custom separators:

```toml
[tool.uv-workspace-dynamic-versioning]
format = "{base}.{distance}"
```

## Other Options

| Option | Description |
|--------|-------------|
| `commit-prefix` | Prefix for commit hash |
| `escape-with` | Character to escape non-alphanumeric |
| `full-commit` | Use full commit hash |
| `commit-length` | Custom commit hash length |
| `dirty` | Force dirty state |
| `metadata` | Include metadata in version |

## Fallback Version

```toml
[tool.uv-workspace-dynamic-versioning]
fallback-version = "0.0.0"
```

Useful for new projects without tags.

## Environment Bypass

```bash
UV_DYNAMIC_VERSIONING_BYPASS=1.0.0 hatch build
```

Overrides version detection entirely.
