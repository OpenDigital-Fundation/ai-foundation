"""Generate PROVENANCE.yaml entries for ported files by matching them against upstream clones.

python -m tools.curation.provenance <sources-dir> <mapping.yaml>

mapping.yaml:
  - dest: domains/workflow/skills/brainstorming      # directory or file in this repo
    source: obra/superpowers
    src: skills/brainstorming                        # directory or file upstream
    files: {modes/inline.md: skills/executing-plans/SKILL.md}   # optional explicit overrides (dest-rel: src-rel)
    extra: [{source, path, modification}]            # optional merged sections applied to the main file
Each dest file gets `base` when byte-identical to its upstream file, otherwise `adapted`.
Files without an upstream match are reported and skipped (they are original work).
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

from tools.catalog import apply


def build(root: Path, sources: Path, mapping: list[dict]) -> dict:
    lock = {s["id"]: s for s in yaml.safe_load((root / "catalog/sources.lock.yaml").read_text())["sources"]}
    out: dict[str, list] = {}
    for m in mapping:
        s = lock[m["source"]]
        clone = sources / m["source"].replace("/", "_")
        dest = root / m["dest"]
        domain = dest.relative_to(root / "domains").parts[0]
        droot = root / "domains" / domain
        files = [dest] if dest.is_file() else sorted(p for p in dest.rglob("*") if p.is_file())
        for f in files:
            rel = f.relative_to(dest).as_posix() if dest.is_dir() else ""
            override = (m.get("files") or {}).get(rel or f.name)
            src_rel = override or (f"{m['src']}/{rel}" if rel else m["src"])
            src = clone / src_rel
            if not src.is_file():
                print(f"original (no upstream match): {f.relative_to(root)}")
                continue
            mod = "base" if src.read_bytes() == f.read_bytes() else "adapted"
            derived = [{"source": m["source"], "commit": s["commit"][:7], "path": src_rel, "license": s["license"], "modification": mod}]
            if f.name in {"SKILL.md"} and rel in {"SKILL.md", ""}:
                for e in m.get("extra") or []:
                    derived.append({"source": e["source"], "commit": lock[e["source"]]["commit"][:7], "path": e["path"],
                                    "license": lock[e["source"]]["license"], "modification": e.get("modification", "merged-section")})
            out.setdefault(domain, []).append({"path": f.relative_to(droot).as_posix(), "derived_from": derived})
    return out


if __name__ == "__main__":
    root = Path(".").resolve()
    prov = build(root, Path(sys.argv[1]), yaml.safe_load(Path(sys.argv[2]).read_text()))
    apply(root, {"provenance": prov})
    for d, fs in prov.items():
        print(f"{d}: {len(fs)} file(s)")
