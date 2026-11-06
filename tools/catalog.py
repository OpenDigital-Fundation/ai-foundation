"""Small helpers to edit catalog/catalog.yaml, catalog/exclusions.yaml and PROVENANCE.yaml.

python -m tools.catalog apply <decisions.yaml>

decisions.yaml:
  artifacts: [{id, type, capability, status?, supersedes: [...]}]
  exclusions: [{key, reason, into?, note?}]
  provenance: {<domain>: [{path, derived_from: [...]}]}
Entries with an existing id/key/path are replaced, so applying twice is idempotent.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

OWNER = "@OpenDigital-Fundation/ai-foundation"


class _Dumper(yaml.SafeDumper):
    pass


_Dumper.add_representer(str, lambda d, s: d.represent_scalar("tag:yaml.org,2002:str", s, style='"' if ":" in s or s != s.strip() else None))


def _dump(path: Path, data) -> None:
    path.write_text(yaml.dump(data, Dumper=_Dumper, sort_keys=False, allow_unicode=True, width=120))


def _upsert(items: list, new: dict, key: str) -> list:
    return [i for i in items if i[key] != new[key]] + [new]


def apply(root: Path, decisions: dict) -> None:
    cat_p, exc_p = root / "catalog/catalog.yaml", root / "catalog/exclusions.yaml"
    cat, exc = yaml.safe_load(cat_p.read_text()), yaml.safe_load(exc_p.read_text())
    cat["artifacts"] = cat.get("artifacts") or []
    exc["excluded"] = exc.get("excluded") or []
    for a in decisions.get("artifacts", []):
        entry = {"id": a["id"], "type": a["type"], "capability": a["capability"],
                 "status": a.get("status", "experimental"), "owner": a.get("owner", OWNER)}
        if a.get("supersedes"):
            entry["supersedes"] = a["supersedes"]
        cat["artifacts"] = _upsert(cat["artifacts"], entry, "id")
    for e in decisions.get("exclusions", []):
        exc["excluded"] = _upsert(exc["excluded"], e, "key")
    cat["artifacts"].sort(key=lambda a: a["id"])
    exc["excluded"].sort(key=lambda e: e["key"].lower())
    _dump(cat_p, cat)
    _dump(exc_p, exc)
    for domain, files in (decisions.get("provenance") or {}).items():
        pp = root / "domains" / domain / "PROVENANCE.yaml"
        prov = yaml.safe_load(pp.read_text())
        prov["files"] = prov.get("files") or []
        for f in files:
            prov["files"] = _upsert(prov["files"], f, "path")
        prov["files"].sort(key=lambda f: f["path"])
        _dump(pp, prov)


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "apply":
        sys.exit(__doc__)
    apply(Path(".").resolve(), yaml.safe_load(Path(sys.argv[2]).read_text()))
