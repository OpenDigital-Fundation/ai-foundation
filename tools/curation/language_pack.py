"""Assemble language packs (one skill per language) from upstream files.

python -m tools.curation.language_pack <sources-dir> catalog/decisions/language-packs.yaml

For each pack writes domains/languages/skills/<lang>/SKILL.md (an index) and references/*.md,
records provenance for every written file, and writes catalog/decisions/languages.yaml with the
artifact and the upstream keys it supersedes. Upstream text is copied with frontmatter removed and
headings demoted one level under a section per source; nothing upstream is executed.
"""
from __future__ import annotations

import csv
import json
import re
import shutil
import sys
from pathlib import Path

import yaml

from tools.catalog import apply

ECC = "affaan-m/ECC"
TOPICS = {
    "standards": ("Standards and idioms", "writing or refactoring code: style, idioms, patterns, project layout"),
    "testing": ("Testing", "writing or fixing tests: runner, fixtures, mocking, coverage"),
    "security": ("Security", "code that handles untrusted input, auth, secrets, files, network or SQL"),
    "review": ("Review checklist", "reviewing a change; read by `code-quality:code-reviewer`"),
    "build": ("Build and dependency errors", "compiler, build tool, type-checker or dependency failures"),
    "tooling": ("Tooling", "formatters, linters, type checkers and editor hooks"),
}
SKIP_LINE = re.compile(r"^\s*(model|tools|color|emoji|vibe):", re.I)


def load_index(root: Path) -> dict[tuple[str, str, str], str]:
    idx: dict[tuple[str, str, str], str] = {}
    for r in csv.DictReader((root / "docs/specs/foundation/source-curation/inventory.csv").open()):
        key = (r["source"], r["kind"], r["name"])
        # prefer the canonical copy over mirrored ones (pi/, .cursor/, plugins/)
        if key not in idx or idx[key].startswith(("pi/", ".", "plugins/")):
            idx[key] = r["path"]
    return idx


def resolve(entry: str, idx) -> tuple[str, str, str]:
    """-> (source, path, inventory key or '')"""
    if re.match(r"^[\w.-]+/[\w.-]+:", entry):
        src, path = entry.split(":", 1)
        name = Path(path).stem
        key = next((f"{s}:{k}:{n}" for (s, k, n), p in idx.items() if s == src and p == path), "")
        return src, path, key
    kind, name = entry.split(":", 1)
    kind = {"s": "skill", "a": "agent", "r": "rule"}[kind]
    if kind == "rule":
        name = name.removesuffix(".md")
    path = idx.get((ECC, kind, name))
    if not path:
        raise SystemExit(f"not in inventory: {entry}")
    return ECC, path, f"{ECC}:{kind}:{name}"


def body_of(text: str) -> tuple[str, str]:
    title = ""
    m = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.S)
    if m:
        fm = yaml.safe_load(m.group(1)) or {}
        title = str(fm.get("name") or "")
        text = text[m.end():]
    h1 = re.search(r"^# (.+)$", text, re.M)
    if h1:
        title = h1.group(1).strip()
        text = text[:h1.start()] + text[h1.end():]
    out, fence = [], False
    for line in text.splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            fence = not fence
        if not fence and line.startswith("#"):
            line = "#" + line
        out.append(line)
    return title, "\n".join(out).strip()


def section(sources_dir: Path, src: str, path: str, lock: dict) -> tuple[str, dict]:
    text = (sources_dir / src.replace("/", "_") / path).read_text(encoding="utf-8")
    title, body = body_of(text)
    title = title or Path(path).stem
    return (f"## {title}\n\n<!-- source: {src} {path} -->\n\n{body}\n",
            {"source": src, "commit": lock[src]["commit"][:7], "path": path, "license": lock[src]["license"], "modification": "adapted"})


COMMAND_TARGET = {"review": "`code-quality:code-review`", "test": "`testing:test-driven-development`",
                  "build": "`debugging:systematic-debugging` with this pack's build reference",
                  "verify": "`testing:verification-before-completion`"}


def reference_map(root: Path, mapping: dict) -> dict[str, str]:
    """Upstream ECC skill/agent names -> where that knowledge lives in this catalog."""
    refs: dict[str, str] = {}
    for entry in yaml.safe_load((root / "catalog/catalog.yaml").read_text()).get("artifacts") or []:
        for key in entry.get("supersedes", []):
            src, kind, name = key.split(":", 2)
            if src == ECC and kind in {"skill", "agent"}:
                refs[name] = f"`{entry['id'].replace('/', ':')}`"
    for lang, pack in mapping["packs"].items():
        groups = list(pack["topics"].items()) + [(f"frameworks/{k}", v) for k, v in (pack.get("frameworks") or {}).items()]
        for topic, entries in groups:
            for e in entries:
                if e[:2] in ("s:", "a:"):
                    refs[e[2:]] = f"`languages:{lang}` (`references/{topic}.md`)"
    return refs


def rewrite_refs(text: str, refs: dict[str, str], unresolved: set[str]) -> str:
    text = re.sub(r"`?/([a-z0-9]+)-(review|test|build|verify)`?", lambda m: COMMAND_TARGET[m.group(2)], text)
    text = text.replace("ECC skills:", "Related:").replace("the ECC philosophy", "these standards")
    text = re.sub(r"ECC's (existing )?`typescript/` rules", "this pack's TypeScript standards", text)
    for a, b in [("Related ECC Skills", "Related skills"), ("Most ECC SWE workflows", "Most general engineering workflows"),
                 ("Streamlined ECC path", "Catalog path"), ("in the ECC repository", "in the upstream repository"),
                 ("bundled with ECC", "bundled with the upstream project"), (" (ECC)", "")]:
        text = text.replace(a, b)

    def sub(m: re.Match) -> str:
        name = m.group(2)
        if name in refs:
            return refs[name]
        if re.search(r"-(patterns|testing|tdd|security|verification|reviewer|build-resolver|standards)$", name):
            unresolved.add(name)
        return m.group(0)
    text = re.sub(r"(`)([a-z0-9]+(?:-[a-z0-9]+)+)`", sub, text)
    text = re.sub(r"(skill: )([a-z0-9]+(?:-[a-z0-9]+)+)", lambda m: "related: " + sub(m), text)
    return text


def build(root: Path, sources_dir: Path, mapping: dict) -> None:
    idx = load_index(root)
    refs = reference_map(root, mapping)
    unresolved: set[str] = set()
    lock = {s["id"]: s for s in yaml.safe_load((root / "catalog/sources.lock.yaml").read_text())["sources"]}
    base = root / "domains/languages/skills"
    provenance, artifacts = [], []
    for lang, pack in mapping["packs"].items():
        d = base / lang
        if d.exists():
            shutil.rmtree(d)  # generated output only; regenerated from the mapping
        (d / "references/frameworks").mkdir(parents=True)
        supersedes: list[str] = []
        rows = []

        def write(rel: str, heading: str, entries: list[str], intro: str) -> None:
            parts, derived = [f"# {pack['title']} — {heading}\n\nPart of `languages:{lang}`. {intro}\n"], []
            for e in entries:
                src, path, key = resolve(e, idx)
                text, prov = section(sources_dir, src, path, lock)
                parts.append(text)
                derived.append(prov)
                if key:
                    supersedes.append(key)
            (d / rel).write_text(rewrite_refs("\n".join(parts).rstrip() + "\n", refs, unresolved), encoding="utf-8")
            provenance.append({"path": f"skills/{lang}/{rel}", "derived_from": derived})

        for topic, entries in pack["topics"].items():
            heading, when = TOPICS[topic]
            write(f"references/{topic}.md", heading, entries, f"Load when {when}.")
            rows.append((f"references/{topic}.md", when))
        fw_rows = []
        for fw, entries in (pack.get("frameworks") or {}).items():
            write(f"references/frameworks/{fw}.md", fw, entries, f"Load only when the project uses {fw}.")
            fw_rows.append(fw)
        if not fw_rows:
            (d / "references/frameworks").rmdir()
        lines = [
            "---", f"name: {lang}", f"description: {json.dumps(pack['description'])}",
            "license: MIT", "metadata:", "  domain: languages", "  status: experimental", "---", "",
            f"# {pack['title']}", "",
            f"Language-specific knowledge for {pack['title']}. The procedures themselves live elsewhere and are not repeated here: "
            "test-first work in `testing:test-driven-development`, review in `code-quality:code-review`, failures in "
            "`debugging:systematic-debugging`, security in `security:security-audit`. This pack adds what is specific to the language.",
            "", "## Load only what the task needs", "", "| Reference | Load when |", "|---|---|",
        ]
        lines += [f"| [`{rel}`]({rel}) | {when} |" for rel, when in rows]
        if fw_rows:
            lines += ["", "## Frameworks", "", "Load the framework file only when the project uses it (check the manifest: "
                      "`package.json`, `pyproject.toml`, `build.gradle`, `Gemfile`, `composer.json`, `pubspec.yaml`, `Package.swift`).", ""]
            lines += [f"- [`{fw}`](references/frameworks/{fw}.md)" for fw in fw_rows]
        lines += ["", "## Precedence", "", "The repository's own standards, linters and `AGENTS.md` override anything in these references. "
                  "When a reference contradicts the code base's established style, follow the code base and mention the difference."]
        (d / "SKILL.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        for cmd in ("review", "test", "build"):
            name = f"{ {'typescript': 'react', 'python': 'python', 'jvm': 'kotlin', 'dart': 'flutter'}.get(lang, lang) }-{cmd}"
            if (ECC, "command", name) in idx:
                supersedes.append(f"{ECC}:command:{name}")
        supersedes += pack.get("also_supersedes", [])
        artifacts.append({"id": f"languages/{lang}", "type": "skill",
                          "capability": f"{pack['title']} patterns, testing, security, review and build knowledge, plus framework references.",
                          "supersedes": sorted(set(supersedes))})
    apply(root, {"provenance": {"languages": provenance}})
    out = root / "catalog/decisions/languages.yaml"
    out.write_text("# Generated by tools.curation.language_pack from catalog/decisions/language-packs.yaml. Do not edit.\n"
                   + yaml.safe_dump({"artifacts": artifacts}, sort_keys=False, width=200, allow_unicode=True))
    print(f"{len(artifacts)} packs, {sum(len(a['supersedes']) for a in artifacts)} upstream items")
    if unresolved:
        print("references to upstream items with no home in the catalog yet:", ", ".join(sorted(unresolved)))


if __name__ == "__main__":
    build(Path(".").resolve(), Path(sys.argv[1]), yaml.safe_load(Path(sys.argv[2]).read_text()))
