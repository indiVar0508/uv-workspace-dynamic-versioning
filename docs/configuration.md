# Configuration

Configuration is managed via the `[tool.hatch.version]` and `[tool.hatch.metadata.hooks.uv-workspace-dynamic-versioning]` sections in `pyproject.toml`.

## Version Source Options

Set these in `[tool.hatch.version]`.

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `vcs` | `string` | `"any"` | VCS to use (`"git"`, `"mercurial"`, `"darcs"`, `"subversion"`, `"fossil"`, `"pijul"`, or `"any"`). |
| `pattern` | `string` | `"default"` | Regex pattern to match tags. |
| `pattern-prefix` | `string` | `null` | Prefix to prepend to the pattern. |
| `format` | `string` | `null` | Custom format string for `dunamai` serialization. |
| `format-jinja` | `string` | `null` | Jinja2 template for the version string. |
| `style` | `string` | `null` | Version style (`"pep440"`, `"semver"`, `"pvp"`). |
| `latest-tag` | `bool` | `false` | Whether to only consider the latest tag. |
| `strict` | `bool` | `false` | Whether to fail if no VCS is found. |
| `tag-dir` | `string` | `"tags"` | Directory where tags are stored (for some VCS). |
| `tag-branch` | `string` | `null` | Branch to look for tags. |
| `full-commit` | `bool` | `false` | Use full commit hash instead of short. |
| `ignore-untracked` | `bool` | `false` | Ignore untracked files when checking for "dirty" state. |
| `commit-length` | `int` | `null` | Length of the commit hash. |
| `bump` | `bool\|dict` | `false` | Configuration for bumping the version if there are commits since the last tag. |
| `fallback-version` | `string` | `null` | Version to use if VCS detection fails. |
| `from-file` | `dict` | `null` | Read version from a file instead of VCS. |

### Bump Configuration

If `bump` is a dictionary:

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `enable` | `bool` | `false` | Enable bumping. |
| `index` | `int` | `-1` | Part of the version to bump. |

### From File Configuration

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `source` | `string` | **Required** | Path to the file. |
| `pattern` | `string` | `null` | Regex to extract the version from the file. |

## Metadata Hook Options

Set these in `[tool.hatch.metadata.hooks.uv-workspace-dynamic-versioning]`.

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `dependencies` | `list[str]` | `null` | List of dependency templates. |
| `optional-dependencies` | `dict[str, list[str]]` | `null` | Dictionary of optional dependency groups and their templates. |

### Jinja2 Context

The following variables are available in Jinja2 templates (`format-jinja`, `dependencies`, `optional-dependencies`):

*   `version`: The `dunamai.Version` object.
    *   `version.base`: The base version (e.g., `0.1.0`).
    *   `version.stage`: The release stage (e.g., `a`, `b`, `rc`).
    *   `version.distance`: Number of commits since the tag.
    *   `version.commit`: Commit hash.
    *   `version.dirty`: Boolean indicating if the repo has uncommitted changes.
*   `config`: The plugin configuration object.
