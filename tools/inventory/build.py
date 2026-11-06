"""Build the upstream inventory and the restricted-licence hash list from fetched sources.

Usage: python -m tools.inventory.build <sources-dir>

Writes:
  docs/specs/foundation/source-curation/inventory.csv  (one row per unique upstream artifact)
  tools/inventory/reference-hashes.txt                 (sha256 of files that must never be copied)
"""
from __future__ import annotations

import csv
import hashlib
import os
import re
import sys
from pathlib import Path

import yaml

from tools.inventory.classify import classify

SKIP_DIRS = {"node_modules", ".git", "tests", "test", "examples", "docs", "i18n", "legacy-command-shims",
             ".openclaw", "cli", "site", "gallery", "preview", "eval", "benchmarks", "translations"}
PROPRIETARY_SKILLS = {"docx", "pdf", "pptx", "xlsx"}
FIELDS = ["source", "kind", "name", "path", "license", "suggested_domain", "description"]


def frontmatter(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8", errors="ignore")
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return None
    y = m.group(1)
    name = re.search(r"^name:\s*[\"']?(.+?)[\"']?\s*$", y, re.M)
    desc = re.search(r"^description:\s*(>-?|\|)?\s*(.*?)(?=^\w[\w-]*:|\Z)", y, re.M | re.S)
    return {"name": name.group(1).strip() if name else None,
            "description": re.sub(r"\s+", " ", desc.group(2)).strip().strip("\"'") if desc else ""}


def kind_of(source_id: str, rel: str, fname: str) -> str | None:
    parent = os.path.dirname(rel)
    if fname == "SKILL.md":
        return "skill"
    if fname.endswith(".md") and re.search(r"(^|/)agents(/|$)", parent):
        return "agent"
    if fname.endswith(".md") and source_id == "msitarzewski/agency-agents" and parent and not parent.startswith(("scripts", "integrations", "examples")):
        return "agent"
    if fname.endswith((".md", ".toml")) and re.search(r"(^|/)commands(/|$)", parent):
        return "command"
    if fname.endswith(".md") and re.search(r"(^|/)rules(/|$)", parent):
        return "rule"
    if fname.endswith((".json", ".js", ".sh", ".py")) and re.search(r"(^|/)hooks(/|$)", parent):
        return "hook"
    if fname.endswith(".json") and re.search(r"mcp", rel, re.I):
        return "mcp"
    return None


def licence_of(source: dict, rel: str, name: str) -> str:
    if source["id"] == "anthropics/skills" and name in PROPRIETARY_SKILLS:
        return "Proprietary (Anthropic)"
    return source["license"]


def build(sources_dir: Path, lock: Path, out_csv: Path, out_hashes: Path) -> None:
    rows, seen, hashes = [], set(), []
    for s in yaml.safe_load(lock.read_text())["sources"]:
        base = sources_dir / s["id"].replace("/", "_")
        if not base.is_dir():
            sys.exit(f"missing clone for {s['id']}; run tools.inventory.fetch first")
        restricted_source = s["policy"] == "reference"
        for dp, dns, fns in os.walk(base):
            dns[:] = sorted(d for d in dns if d not in SKIP_DIRS and not (d.startswith(".") and d != ".claude"))
            for f in sorted(fns):
                p = Path(dp) / f
                rel = str(p.relative_to(base))
                kind = kind_of(s["id"], rel, f)
                fm = frontmatter(p) if f.endswith(".md") and kind else None
                name = (fm or {}).get("name") or (p.parent.name if f == "SKILL.md" else p.stem)
                if kind == "rule":  # rules have no frontmatter and repeat file names across languages
                    m = re.search(r"(?:^|/)rules/(.+)\.md$", rel)
                    name = m.group(1) if m else p.stem
                lic = licence_of(s, rel, name if f == "SKILL.md" else "")
                if (restricted_source or lic.startswith("Proprietary")) and p.stat().st_size > 64 and p.suffix in {".md", ".py", ".js", ".ts", ".json", ".yaml", ".yml", ".txt", ".sh"}:
                    hashes.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()} {s['id']}:{rel}")
                if not kind or (kind in {"skill", "agent"} and not fm):
                    continue
                desc = (fm or {}).get("description", "")
                key = (s["id"], kind, name, desc[:80] or rel)
                if key in seen:
                    continue
                seen.add(key)
                division = rel.split("/")[0] if s["id"] == "msitarzewski/agency-agents" else ""
                rows.append({"source": s["id"], "kind": kind, "name": name, "path": rel, "license": lic,
                             "suggested_domain": classify(name, kind, rel, division), "description": desc[:240]})
    rows.sort(key=lambda r: (r["suggested_domain"], r["kind"], r["name"].lower(), r["source"]))
    with out_csv.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    out_hashes.write_text("# sha256 <source>:<path> of files from reference-only or proprietary sources. Generated.\n"
                          + "\n".join(sorted(set(hashes))) + "\n")
    print(f"{len(rows)} artifacts -> {out_csv}; {len(set(hashes))} restricted hashes -> {out_hashes}")


if __name__ == "__main__":
    build(Path(sys.argv[1]), Path("catalog/sources.lock.yaml"),
          Path("docs/specs/foundation/source-curation/inventory.csv"), Path("tools/inventory/reference-hashes.txt"))
