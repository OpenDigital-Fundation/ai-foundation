"""Copy an upstream skill directory into a domain and apply catalog/renames.yaml.

python -m tools.curation.port <upstream-dir> <domain> <new-name>

The frontmatter `name` is rewritten and `metadata.domain/status` added. Everything else is
copied verbatim (minus the substitutions) so that the remaining edits are reviewable as a diff
against upstream. Prints the files written.
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

import yaml

TEXT = {".md", ".txt", ".yaml", ".yml", ".sh", ".js", ".cjs", ".ts", ".py", ".html"}


def substitutions(root: Path) -> list[tuple[str, str]]:
    r = yaml.safe_load((root / "catalog/renames.yaml").read_text())
    pairs = list(r["references"].items()) + list(r["text"].items())
    return sorted(pairs, key=lambda p: -len(p[0]))  # longest first


def port(root: Path, src: Path, domain: str, name: str) -> list[Path]:
    dest = root / "domains" / domain / "skills" / name
    if dest.exists():
        sys.exit(f"{dest} already exists")
    shutil.copytree(src, dest, ignore=shutil.ignore_patterns("LICENSE*", ".*", "agents"))
    subs = substitutions(root)
    written = []
    for p in sorted(dest.rglob("*")):
        if p.is_file() and p.suffix in TEXT:
            t = p.read_text(encoding="utf-8")
            for a, b in subs:
                t = t.replace(a, b)
            if p.name == "SKILL.md":
                t = _frontmatter(t, name, domain)
            p.write_text(t, encoding="utf-8")
        written.append(p)
    return written


def _frontmatter(text: str, name: str, domain: str) -> str:
    m = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.S)
    fm = yaml.safe_load(m.group(1)) if m else {}
    fm["name"] = name
    fm.setdefault("license", "MIT")
    fm["metadata"] = {**(fm.get("metadata") or {}), "domain": domain, "status": "experimental"}
    order = ["name", "description", "license", "metadata"]
    fm = {k: fm[k] for k in order if k in fm} | {k: v for k, v in fm.items() if k not in order}
    head = yaml.safe_dump(fm, sort_keys=False, width=1000, allow_unicode=True)
    return f"---\n{head}---\n" + (text[m.end():] if m else text)


if __name__ == "__main__":
    root = Path(".").resolve()
    for p in port(root, Path(sys.argv[1]), sys.argv[2], sys.argv[3]):
        print(p.relative_to(root))
