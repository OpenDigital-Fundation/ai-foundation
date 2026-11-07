"""Canonical support-file paths inside independently installable artifacts."""
from __future__ import annotations

import re
from pathlib import Path

TEXT = {".md", ".txt", ".yaml", ".yml", ".json", ".py", ".js", ".mjs", ".cjs", ".html", ".sh", ".toml"}


def normalize(directory: Path) -> dict[str, str]:
    moves = {p.relative_to(directory).as_posix(): p.with_name("README.md").relative_to(directory).as_posix()
             for p in sorted((directory / "references").rglob("SKILL.md"))}
    fonts = directory / "canvas-fonts"
    if fonts.is_dir():
        moves.update({p.relative_to(directory).as_posix(): "assets/fonts/" + p.relative_to(fonts).as_posix()
                      for p in sorted(fonts.rglob("*")) if p.is_file()})
    if not moves:
        return {}
    # Check the entire batch before renaming. Never overwrite an existing reference or asset.
    for old, new in moves.items():
        if (directory / new).exists():
            raise ValueError(f"normalization collision: {directory / old} -> {new}")
    resolved = {(directory / old).resolve(): (directory / new).resolve() for old, new in moves.items()}
    edits = {}
    for path in sorted(directory.rglob("*")):
        if not path.is_file() or path.suffix not in TEXT:
            continue
        text = path.read_text(encoding="utf-8")
        # Explicit root-relative paths also occur in code spans and command examples.
        for old, new in moves.items():
            text = text.replace(old, new)
        if fonts.is_dir():
            text = text.replace("canvas-fonts", "assets/fonts")

        def relink(match: re.Match) -> str:
            link = match.group(1)
            target, separator, fragment = link.partition("#")
            destination = resolved.get((path.parent / target).resolve())
            if destination is None:
                return match.group(0)
            import os
            new_parent = resolved.get(path.resolve(), path.resolve()).parent
            return "](" + Path(os.path.relpath(destination, new_parent)).as_posix() + (separator + fragment if separator else "") + ")"

        text = re.sub(r"\]\((?!https?://|#|mailto:)([^)\s]+)\)", relink, text)
        edits[path] = text
    for path, text in edits.items():
        if text != path.read_text(encoding="utf-8"):
            path.write_text(text, encoding="utf-8")
    for old, new in moves.items():
        target = directory / new
        target.parent.mkdir(parents=True, exist_ok=True)
        (directory / old).rename(target)
    return moves


def remap_provenance(entries: list[dict], prefix: str, moves: dict[str, str]) -> None:
    destinations = {f"{prefix}/{old}": f"{prefix}/{new}" for old, new in moves.items()}
    for entry in entries:
        entry["path"] = destinations.get(entry["path"], entry["path"])


def upstream_path(clone: Path, original: str) -> str:
    """Find renamed support files in a pinned upstream without changing its recorded path."""
    if (clone / original).is_file():
        return original
    candidate = original.replace("assets/fonts/", "canvas-fonts/")
    if candidate.endswith("/README.md"):
        skill = candidate.removesuffix("README.md") + "SKILL.md"
        if (clone / skill).is_file():
            return skill
    return candidate if (clone / candidate).is_file() else original
