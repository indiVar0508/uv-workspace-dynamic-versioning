# Jinja2 Templating Example

This example demonstrates using Jinja2 templates for custom version formatting.

## Available Template Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `version` | Full Version object | `Version(...)` |
| `base` | Base version string | `"1.2.3"` |
| `major` | Major version part | `1` |
| `minor` | Minor version part | `2` |
| `patch` | Patch version part | `3` |
| `stage` | Version stage | `"a"`, `"rc"` |
| `revision` | Revision number | `1` |
| `distance` | Commits since tag | `5` |
| `commit` | Truncated commit hash | `"abc1234"` |
| `dirty` | Is working dir dirty | `true`/`false` |
| `branch` | Current branch name | `"feature-x"` |
| `tagged_metadata` | Metadata from tag | `"anything"` |
| `timestamp` | Formatted timestamp | `"20240301120000"` |

## Example Templates

**Simple:**
```toml
format-jinja = "v{{ major }}.{{ minor }}.{{ patch }}"
# Output: v1.2.3
```

**With branch:**
```toml
format-jinja = "{{ major }}.{{ minor }}.{{ patch }}+{{ branch | default('main') }}"
escape-with = "."
# Output: 1.2.3+feature-x
```

**PEP 440 compliant:**
```toml
format-jinja = "{{ major }}.{{ minor }}.{{ patch }}.dev{{ distance }}"
# Output: 1.2.3.dev5
```

## Usage

```bash
hatch build
# or
uv build
```
