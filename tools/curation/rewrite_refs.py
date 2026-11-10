"""Rewrite upstream skill/agent/command references to catalog artifacts in ported markdown.

python -m tools.curation.rewrite_refs <dir>...   (uses catalog supersedes and language-pack membership)
Prints references that still have no home in the catalog.
"""
import sys
from pathlib import Path

import yaml

from tools.curation.language_pack import reference_map, rewrite_refs

if __name__ == "__main__":
    root = Path(".").resolve()
    from tools.curation.manifests import language_packs
    refs = reference_map(root, language_packs(root))
    unresolved: set[str] = set()
    for d in sys.argv[1:]:
        for f in Path(d).rglob("*.md"):
            t = f.read_text(encoding="utf-8")
            n = rewrite_refs(t, refs, unresolved)
            if n != t:
                f.write_text(n, encoding="utf-8")
                print(f"rewrote {f}")
    if unresolved:
        print("unresolved:", ", ".join(sorted(unresolved)))
