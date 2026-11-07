"""Compare each pinned source with its current HEAD and report inventory changes as Markdown.

python -m tools.inventory.sync_report <work-dir> [--out report.md]

Never updates content: the report is reviewed by a person, who updates sources.lock.yaml and the
affected decisions in a normal pull request.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import re
import subprocess
import sys
from pathlib import Path

import yaml

from tools.inventory.build import build
from tools.inventory.fetch import fetch


SAFE = re.compile(r"[A-Za-z0-9 ._/&()+:-]{1,200}")


def safe(value: str) -> str:
    """Upstream names end up in a GitHub issue: keep a strict charset, neutralise @mentions, else show a hash."""
    value = value.replace("@", "(at)")
    if SAFE.fullmatch(value):
        return f"`{value}`"
    return f"`sha256:{hashlib.sha256(value.encode()).hexdigest()[:16]}` (name withheld: unexpected characters)"


def remote_head(url: str) -> str:
    out = subprocess.run(["git", "ls-remote", url, "HEAD"], capture_output=True, text=True, timeout=60, check=True).stdout
    return out.split()[0]


def rows(path: Path) -> dict[str, dict]:
    return {f"{r['source']}:{r['kind']}:{r['name']}": r for r in csv.DictReader(path.open())}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("work")
    ap.add_argument("--out", default="-")
    args = ap.parse_args(argv)
    root, work = Path(".").resolve(), Path(args.work).resolve()
    lock = yaml.safe_load((root / "catalog/sources.lock.yaml").read_text())
    moved = []
    for s in lock["sources"]:
        head = remote_head(s["url"])
        if head != s["commit"]:
            moved.append((s["id"], s["commit"], head))
            s["commit"] = head
    lines = ["# Upstream sync report", ""]
    if not moved:
        lines.append("All sources are at their pinned commit. Nothing to review.")
    else:
        head_lock = work / "sources.head.yaml"
        head_lock.write_text(yaml.safe_dump(lock, sort_keys=False))
        fetch(head_lock, work / "sources")
        head_csv = work / "inventory.head.csv"
        build(work / "sources", head_lock, head_csv, work / "reference-hashes.head.txt")
        old, new = rows(root / "catalog/inventory/artifacts.csv"), rows(head_csv)
        moved_ids = {m[0] for m in moved}
        lines += ["| Source | Pinned | HEAD |", "|---|---|---|"] + [f"| {safe(i)} | `{a[:7]}` | `{b[:7]}` |" for i, a, b in moved] + [""]
        added = sorted(k for k in new if k not in old)
        removed = sorted(k for k in old if k not in new and k.split(":")[0] in moved_ids)
        changed = sorted(k for k in new if k in old and new[k]["description"] != old[k]["description"])
        for title, keys in (("New upstream artifacts (need a decision)", added), ("Removed upstream", removed),
                            ("Changed description", changed)):
            lines += [f"## {title} ({len(keys)})", ""] + [f"- {safe(k)}" for k in keys[:200]] + [""]
        # Upstream files this catalog derives from (PROVENANCE.yaml) that changed between pinned and HEAD.
        pinned = {i: a for i, a, _ in moved}
        derived: dict[str, set[str]] = {}
        for prov in sorted(root.glob("domains/*/PROVENANCE.yaml")):
            for f in yaml.safe_load(prov.read_text()).get("files") or []:
                for d in f["derived_from"]:
                    if d["source"] in pinned:
                        derived.setdefault(d["source"], set()).add(d["path"])
        touched = []
        for sid, old_commit in pinned.items():
            repo = work / "sources" / sid.replace("/", "_")
            subprocess.run(["git", "-C", str(repo), "fetch", "-q", "--depth", "1", "origin", old_commit], check=True, timeout=300)
            names = subprocess.run(["git", "-C", str(repo), "diff", "--name-only", old_commit, "HEAD"],
                                   capture_output=True, text=True, check=True).stdout.split()
            touched += sorted(f"{sid}:{n}" for n in names if n in derived.get(sid, set()))
        lines += [f"## Upstream files we derive from that changed ({len(touched)})", ""] + [f"- {safe(k)}" for k in touched] + [""]
        lines += ["Next: review, bump `catalog/sources.lock.yaml`, regenerate the inventory and decide every new key; "
                  "for changed derived files, compare upstream with ours and port what improves them."]
    text = "\n".join(lines) + "\n"
    if args.out == "-":
        sys.stdout.write(text)
    else:
        Path(args.out).write_text(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
