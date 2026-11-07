"""Validate recipe inputs before any generated directory is replaced."""
from __future__ import annotations

import re
from pathlib import Path


def preflight(root: Path, sources: Path, recipes: dict, packs: dict | None = None) -> None:
    from tools.curation.bundle import _resolve
    from tools.curation.language_pack import ECC, TOPICS, load_index, resolve, section
    from tools.curation.manifests import load
    import yaml

    idx = load_index(root)
    lock = {s["id"]: s for s in yaml.safe_load((root / "catalog/sources.lock.yaml").read_text())["sources"]}
    declared = {a["id"]: set(a.get("supersedes", [])) for m in load(root).values() for a in m["artifacts"]}

    def source(src: str, path: str, directory: bool = False) -> Path:
        if src not in lock or lock[src]["policy"] != "merge":
            raise ValueError(f"source '{src}' is not approved for copying")
        clone = (sources / src.replace("/", "_")).resolve()
        target = (clone / path).resolve()
        if not target.is_relative_to(clone):
            raise ValueError(f"source path escapes its clone: {src}:{path}")
        if not (target.is_dir() if directory else target.is_file()):
            raise ValueError(f"missing source {'directory' if directory else 'file'}: {src}:{path}")
        return target

    def owns(aid: str, keys: set[str]) -> None:
        if aid not in declared:
            raise ValueError(f"recipe has no editorial artifact: {aid}")
        missing = keys - {""} - declared[aid]
        if missing:
            raise ValueError(f"{aid}: recipe items missing from manifest supersedes: {sorted(missing)}")

    for aid, recipe in recipes.items():
        keys = set(recipe.get("supersedes", []))
        for pattern in recipe.get("remove", []):
            re.compile(pattern, re.S | re.M)
        for pattern, replacement in recipe.get("replace", []):
            re.sub(pattern, replacement, "", flags=re.S | re.M)
        if recipe.get("base"):
            src, path, key = _resolve(recipe["base"], idx)
            source(src, path).read_text(encoding="utf-8")
            keys.add(key)
        if recipe.get("base_dir"):
            src, path = recipe["base_dir"].split(":", 1)
            directory = source(src, path, directory=True)
            source(src, f"{path}/SKILL.md").read_text(encoding="utf-8")
            for file in directory.rglob("*"):
                if file.is_file() and file.suffix in {".md", ".py", ".txt", ".sh", ".js", ".mjs"}:
                    file.read_text(encoding="utf-8")
            keys.update(f"{s}:{kind}:{name}" for (s, kind, name), p in idx.items() if s == src and p == f"{path}/SKILL.md")
        for relative, entries in (recipe.get("references") or {}).items():
            _relative(relative)
            for entry in entries:
                src, path, key = _resolve(entry, idx)
                source(src, path)
                section(sources, src, path, lock)
                keys.add(key)
        for relative, entry in (recipe.get("reference_dirs") or {}).items():
            _relative(relative)
            src, path = entry.split(":", 1)
            source(src, path, directory=True)
            keys.update(f"{s}:{kind}:{name}" for (s, kind, name), p in idx.items()
                        if s == src and (p == path or p.startswith(path.rstrip("/") + "/")))
        owns(aid, keys)

    for lang, pack in (packs or {}).items():
        keys = set(pack.get("also_supersedes", []))
        for topic in pack["topics"]:
            if topic not in TOPICS:
                raise ValueError(f"languages/{lang}: unknown language topic '{topic}'")
        for framework in pack.get("frameworks", {}):
            _relative(framework)
        for entries in list(pack["topics"].values()) + list((pack.get("frameworks") or {}).values()):
            for entry in entries:
                src, path, key = resolve(entry, idx)
                source(src, path)
                section(sources, src, path, lock)
                keys.add(key)
        for command in ("review", "test", "build"):
            name = f"{ {'typescript': 'react', 'jvm': 'kotlin', 'dart': 'flutter'}.get(lang, lang) }-{command}"
            if (ECC, "command", name) in idx:
                keys.add(f"{ECC}:command:{name}")
        owns(f"languages/{lang}", keys)


def _relative(path: str) -> None:
    value = Path(path)
    if value.is_absolute() or ".." in value.parts or not value.parts:
        raise ValueError(f"output path must be relative and stay inside its artifact: {path}")
