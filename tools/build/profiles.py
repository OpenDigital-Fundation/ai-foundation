"""Resolve profiles (cross-domain bundles) to the plugins and artifacts they need."""
from __future__ import annotations

from fnmatch import fnmatch
from pathlib import Path

import yaml

from tools.build.marketplace import MARKETPLACE


def resolve(root: Path, profile: str) -> dict:
    spec = yaml.safe_load((root / "profiles" / f"{profile}.yaml").read_text())
    catalog = yaml.safe_load((root / "catalog/catalog.yaml").read_text()).get("artifacts") or []
    ids = [a["id"] for a in catalog if a["status"] != "deprecated"]
    selected = sorted({i for pattern in spec["include"] for i in ids if fnmatch(i, pattern)})
    plugins = sorted({i.split("/")[0] for i in selected} | {p.split("/")[0] for p in spec["include"]})
    return {"name": spec["name"], "plugins": plugins, "artifacts": selected,
            "install": [f"/plugin install {p}@{MARKETPLACE}" for p in plugins]}
