"""Turn relative Markdown links that do not resolve into plain text (the label is kept).

Used after assembling files from upstream: concatenated references inherit links to upstream
files that were not copied. python -m tools.curation.links <dir>... fixes files in place.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

LINK = re.compile(r"(!?)\[([^\]\n]*)\]\((?!https?://|#|mailto:)([^)\s]+)\)")
FENCE = re.compile(r"(?ms)^(```|~~~).*?^\1")


def unlink_missing(text: str, path: Path) -> str:
    parts, last = [], 0
    for m in FENCE.finditer(text):  # leave code blocks untouched
        parts.append((text[last:m.start()], True))
        parts.append((m.group(0), False))
        last = m.end()
    parts.append((text[last:], True))

    def fix(m: re.Match) -> str:
        target = (path.parent / m.group(3).split("#")[0]).resolve()
        if m.group(3).split("#")[0] == "" or target.exists():
            return m.group(0)
        return m.group(2) if not m.group(1) else ""
    return "".join(LINK.sub(fix, chunk) if prose else chunk for chunk, prose in parts)


if __name__ == "__main__":
    for d in sys.argv[1:]:
        for f in Path(d).rglob("*.md"):
            t = f.read_text(encoding="utf-8", errors="ignore")
            n = unlink_missing(t, f)
            if n != t:
                f.write_text(n, encoding="utf-8")
                print(f"fixed {f}")
