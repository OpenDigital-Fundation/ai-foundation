"""Small helpers to edit catalog/catalog.yaml, catalog/exclusions.yaml and PROVENANCE.yaml.

python -m tools.catalog apply <decisions.yaml>
python -m tools.catalog rebuild     regenerate catalog.yaml and exclusions.yaml from catalog/decisions/*.yaml

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


def rebuild(root: Path) -> None:
    """Decision files are the source of truth; catalog.yaml and exclusions.yaml are derived."""
    (root / "catalog/catalog.yaml").write_text("version: 1\nartifacts: []\n")
    (root / "catalog/exclusions.yaml").write_text("version: 1\nexcluded: []\n")
    extends: dict[str, list[str]] = {}
    for f in sorted((root / "catalog/decisions").glob("*.yaml")):
        data = yaml.safe_load(f.read_text())
        if isinstance(data, dict) and ("artifacts" in data or "exclusions" in data):
            apply(root, {k: data[k] for k in ("artifacts", "exclusions") if k in data})
        if isinstance(data, dict) and data.get("extend"):
            for aid, keys in data["extend"].items():
                extends.setdefault(aid, []).extend(keys)
    if extends:  # applied last so it never depends on file order
        cat_p = root / "catalog/catalog.yaml"
        cat = yaml.safe_load(cat_p.read_text())
        for entry in cat["artifacts"]:
            if entry["id"] in extends:
                entry["supersedes"] = sorted(set(entry.get("supersedes", [])) | set(extends.pop(entry["id"])))
        if extends:
            raise SystemExit(f"extend targets not in catalog: {sorted(extends)}")
        _dump(cat_p, cat)


if __name__ == "__main__":
    root = Path(".").resolve()
    if sys.argv[1:] == ["rebuild"]:
        rebuild(root)
    elif len(sys.argv) == 3 and sys.argv[1] == "apply":
        apply(root, yaml.safe_load(Path(sys.argv[2]).read_text()))
    else:
        sys.exit(__doc__)
