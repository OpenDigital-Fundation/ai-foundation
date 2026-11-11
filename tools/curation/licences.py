"""Effective licence of upstream files and the copy gate used by every curation route.

The lock records one licence per collection; collections such as openai/skills or
getsentry/skills declare different terms per folder. The nearest LICENSE file wins, and a
file that itself declares it derives from ShareAlike or non-commercial text is refused even
inside a permissive folder.
"""
from __future__ import annotations

import re
from pathlib import Path

from tools.inventory.build import is_permissive, nearest_licence, same_licence

_RESTRICTED_NOTICE = re.compile(r"(?:based on|derived from|adapted from|excerpted from|licensed under|licence[d]?:|license[d]?:)[^\n]{0,160}?(?:CC[ -]BY[ -](?:NC|SA)|Attribution-(?:ShareAlike|NonCommercial))", re.I)
_TEXT = {".md", ".txt", ".markdown", ".rst"}


def _clone(sources: Path, src: str) -> Path:
    return sources / src.replace("/", "_")


_CODE_TEXT = {".tex", ".bst", ".sty", ".py", ".sh", ".js", ".ts", ".c", ".h", ".cpp", ".rs", ".go", ".rb", ".java"}


def _inline_licence(file: Path) -> str | None:
    if not file.is_file() or file.suffix.lower() not in (_CODE_TEXT | _TEXT):
        return None
    head = file.read_text(encoding="utf-8", errors="ignore")[:4096]
    normalized = re.sub(r"(?m)^\s*(?:%+|#+|//+|/\*+|\*+)\s?", "", head)
    spdx = re.search(r"(?m)^SPDX-License-Identifier:\s*([^\n]+)", normalized)
    if spdx:
        value = spdx.group(1).removesuffix("*/").strip()
        return value if re.fullmatch(r"[A-Za-z0-9.+-]+", value) else f"Restricted (SPDX expression: {value})"
    flat = re.sub(r"\s+", " ", normalized)
    notice = re.search(r"(?:may be (?:re)?distributed|licensed) .{0,180}?LaTeX Project Public License", flat, re.I)
    if notice:
        version = re.search(r"version\s+(1\.\d[a-z]?)", flat[notice.end():notice.end()+160], re.I)
        return "LPPL-" + (version.group(1) if version else "unspecified")
    return None


def effective_licence(lock: dict, sources: Path, src: str, path: str) -> str:
    clone = _clone(sources, src)
    target = clone / path
    inline = _inline_licence(target)
    if inline:
        return inline
    probe = target / "_" if target.is_dir() else target
    return nearest_licence(clone, probe) or lock[src]["license"]


def _allowed(licence: str, accepted: str) -> bool:
    if is_permissive(licence):
        return True
    # A restricted licence is copyable only when the maintainer accepted exactly it in the lock.
    return not is_permissive(accepted) and accepted != "NOASSERTION" and same_licence(licence, accepted)


def check_copy(lock: dict, sources: Path, src: str, path: str, *, exclude: set[str] | None = None) -> str:
    """Return the effective licence of `path` (file or folder), or raise when copying is not permitted."""
    clone = _clone(sources, src)
    target = clone / path
    files = sorted(p for p in target.rglob("*") if p.is_file() and not p.name.upper().startswith(("LICENSE", "LICENCE", "COPYING"))) if target.is_dir() else [target]
    if exclude:
        files = [f for f in files if f.relative_to(target).as_posix() not in exclude]
    accepted = lock[src]["license"]
    licences = set()
    for f in files:
        rel = f.relative_to(clone).as_posix()
        lic = effective_licence(lock, sources, src, rel)
        if not _allowed(lic, accepted):
            raise ValueError(f"licence '{lic}' of {src}:{rel} does not permit copying")
        if f.suffix.lower() in _TEXT and _RESTRICTED_NOTICE.search(f.read_text(encoding="utf-8", errors="ignore")[:4000]):
            raise ValueError(f"{src}:{rel} declares ShareAlike or non-commercial origin; it does not permit copying")
        licences.add(lic)
    if not files:
        licences.add(effective_licence(lock, sources, src, path))
    return sorted(licences)[0] if len(licences) == 1 else " + ".join(sorted(licences))
