from __future__ import annotations

import contextlib
import os
import re
from datetime import datetime
from importlib import import_module

import jinja2
import jinja2.sandbox
from dunamai import (
    Version,
    bump_version,
    serialize_pep440,
    serialize_pvp,
    serialize_semver,
)

from . import schemas

_JINJA_ENV = jinja2.sandbox.SandboxedEnvironment()


def base_part(base: str, index: int) -> int:
    parts = base.split(".")
    result = 0

    with contextlib.suppress(KeyError, ValueError):
        result = int(parts[index])

    return result


def _escape_branch(value: str | None, escape_with: str | None) -> str | None:
    if value is None:
        return None

    return re.sub(r"[^a-zA-Z0-9]", escape_with or "", value)


def _format_timestamp(value: datetime | None) -> str | None:
    if value is None:
        return None

    return value.strftime("%Y%m%d%H%M%S")


def render_template(
    template: str, *, version: Version, config: schemas.UvWorkspaceDynamicVersioning
) -> str:
    default_context = {
        "version": version,
        "base": version.base,
        "stage": version.stage,
        "revision": version.revision,
        "distance": version.distance,
        "commit": version.commit,
        "dirty": version.dirty,
        "branch": version.branch,
        "tagged_metadata": version.tagged_metadata,
        "branch_escaped": _escape_branch(version.branch, config.escape_with),
        "timestamp": _format_timestamp(version.timestamp),
        "major": base_part(version.base, 0),
        "minor": base_part(version.base, 1),
        "patch": base_part(version.base, 2),
        "bump_version": bump_version,
        "serialize_pep440": serialize_pep440,
        "serialize_pvp": serialize_pvp,
        "serialize_semver": serialize_semver,
    }

    custom_context = {}
    if config.format_jinja_imports:
        for entry in config.format_jinja_imports:
            try:
                module = import_module(entry.module)
            except ImportError as e:
                raise ValueError(f"Failed to import module '{entry.module}': {e}") from None

            if entry.item is not None:
                try:
                    custom_context[entry.item] = getattr(module, entry.item)
                except AttributeError:
                    raise ValueError(
                        f"Module '{entry.module}' has no item '{entry.item}'"
                    ) from None
            else:
                custom_context[entry.module] = module

    return _JINJA_ENV.from_string(template).render(**default_context, **custom_context)
