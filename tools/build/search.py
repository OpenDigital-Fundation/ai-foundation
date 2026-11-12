"""Generate the private portable search projection from public catalog metadata."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import runpy

import yaml

from tools.validate.repo import discover

SKILL = Path("domains/agent-engineering/skills/skill-discovery")
INDEX = SKILL / "assets/catalog-index.json"


def build(root: Path) -> dict:
    entries = yaml.safe_load((root / "catalog/catalog.yaml").read_text())["artifacts"]
    terms = json.loads((root / SKILL / "assets/search-terms.json").read_text())
    ids = {a["id"] for a in entries}
    if not isinstance(terms, dict) or set(terms) - ids:
        raise ValueError("internal search terms must belong to existing catalog IDs")
    if any(not isinstance(v, list) or not all(isinstance(t, str) and t.strip() for t in v) for v in terms.values()):
        raise ValueError("internal search terms must be lists of nonempty strings")
    arts = {a.id: a for a in discover(root)}
    facets = yaml.safe_load((root / "catalog/facets.yaml").read_text())["artifacts"]
    vocab = {p.stem: {t["id"]: t for t in yaml.safe_load(p.read_text())["terms"]}
             for p in sorted((root / "catalog/taxonomy").glob("*.yaml"))}
    out = []
    for a in sorted(entries, key=lambda a: a["id"]):
        art = arts[a["id"]]
        labels = []
        for facet, values in facets.get(a["id"], {}).items():
            for value in values:
                term = vocab.get(facet, {}).get(value, {})
                labels += [value] + list(term.get("name", {}).values())
        out.append({"id": a["id"], "domain": art.domain, "type": a["type"], "status": a["status"],
                    "description": a["capability"], "path": art.path.relative_to(root).as_posix(),
                    "terms": terms.get(a["id"], []), "facets": sorted(set(labels)),
                    "sources": sorted({k.split(":")[0] for k in a.get("supersedes", [])})})
    digest = hashlib.sha256(json.dumps(out, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    return {"version": 1, "generated_by": "python -m tools.build docs", "source_digest": digest, "artifacts": out}


def render(root: Path) -> str:
    return json.dumps(build(root), ensure_ascii=False, indent=2) + "\n"


def write(root: Path) -> Path | None:
    if not (root / SKILL).is_dir():
        return None
    target = root / INDEX
    target.write_text(render(root))
    return target


def check(root: Path) -> list[str]:
    if not (root / SKILL).is_dir():
        return []
    try:
        expected = render(root)
        actual = (root / INDEX).read_text()
    except (OSError, ValueError, KeyError, TypeError) as error:
        return [f"{INDEX}: {error}"]
    return [] if expected == actual else [f"{INDEX}: stale index; run python -m tools.build docs"]


def find(root: Path, argv: list[str]) -> int:
    # One search implementation, also distributed with the skill; this path never invokes third-party code.
    module = runpy.run_path(str(root / SKILL / "scripts/find.py"))
    return module["main"](argv, index=build(root))
