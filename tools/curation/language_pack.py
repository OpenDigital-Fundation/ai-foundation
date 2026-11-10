"""Assemble language packs (one skill per language) from upstream files.

python -m tools.curation <sources-dir> --domain languages

For each pack writes domains/languages/skills/<lang>/SKILL.md (an index) and references/*.md,
records provenance for every written file. Registry metadata and supersedes are edited in
catalog/curation/domains/languages.yaml. Upstream text is copied with frontmatter removed and
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
    for r in csv.DictReader((root / "catalog/inventory/artifacts.csv").open()):
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
    from tools.curation.licences import effective_licence
    text = (sources_dir / src.replace("/", "_") / path).read_text(encoding="utf-8")
    title, body = body_of(text)
    title = title or Path(path).stem
    return (f"## {title}\n\n<!-- source: {src} {path} -->\n\n{body}\n",
            {"source": src, "commit": lock[src]["commit"][:7], "path": path, "license": effective_licence(lock, sources_dir, src, path), "modification": "adapted"})


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


PERSONA_SECTION = re.compile(
    r"^(#{2,3}) [^\n]*(Your Identity|Identity & Memory|Communication Style|Learning & Memory|Your Personality|Personality)\b[^\n]*\n.*?(?=^#{1,3} |\Z)",
    re.M | re.S)


def strip_persona(text: str) -> str:
    """Drop persona-only sections (identity, personality, communication style, memory) from agent profiles."""
    return PERSONA_SECTION.sub("", text)


def rewrite_refs(text: str, refs: dict[str, str], unresolved: set[str]) -> str:
    text = strip_persona(text)
    text = re.sub(r"`?/([a-z0-9]+)-(review|test|build|verify)`?", lambda m: COMMAND_TARGET[m.group(2)], text)
    text = text.replace("ECC skills:", "Related:").replace("the ECC philosophy", "these standards")
    text = re.sub(r"ECC's (existing )?`typescript/` rules", "this pack's TypeScript standards", text)
    for a, b in [("Related ECC Skills", "Related skills"), ("Most ECC SWE workflows", "Most general engineering workflows"),
                 ("Streamlined ECC path", "Catalog path"), ("in the ECC repository", "in the upstream repository"),
                 ("bundled with ECC", "bundled with the upstream project"), (" (ECC)", ""),
                 ("ECC-native skills", "catalog skills"), ("ECC-native lane", "catalog skill"), ("ECC lane", "catalog skill"),
                 ("the canonical ECC SEO workflow", "the canonical SEO workflow"), ("ECC or website", "product or website"),
                 ("inside ECC", "inside this catalog"), (", and ECC 2.0", ""), ("ECC 2.0", "")]:
        text = text.replace(a, b)
    # Pin package executions that upstream wrote as @latest (reviewed versions or an explicit placeholder).
    for pkg, pinned in [("shadcn-ui@latest", "shadcn@2.3.0"), ("shadcn@latest", "shadcn@2.3.0"),
                        ("@angular/cli@latest", "@angular/cli@<version>"),
                        ("@modelcontextprotocol/codemod@latest", "@modelcontextprotocol/codemod@<version>")]:
        text = text.replace(pkg, pinned)
    # Versions belong to the consuming project; never silently install the newest release.
    for package in ("@apollo/client", "graphql", "@emotion/react", "@emotion/styled", "react-router-dom", "<package>"):
        text = text.replace(f"{package}@latest", f"{package}@<version>")
    text = text.replace("go get github.com/modelcontextprotocol/go-sdk@latest",
                        "# Select a reviewed SDK version compatible with the project before running.\ngo get github.com/modelcontextprotocol/go-sdk@<version>")
    text = text.replace("COPY --from=composer:latest", "COPY --from=composer:<version>")
    text = text.replace("image: myapp:latest", "image: myapp:<release-tag>")
    # A failed install is evidence to report, not a reason to claim the dependency was unused.
    text = re.sub(r'^(\s*npm install[^\n]*?) 2>/dev/null(?: && echo [^\n]*)?$', r"\1", text, flags=re.M)
    text = re.sub(r"^.*\bAffaan\b.*\n", "", text, flags=re.M)  # lines about the upstream author's own voice or setup
    text = re.sub(r"(?<!source: affaan-m/)\bECC\b(?!-)", "the upstream project", text)

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
    from tools.curation.inputs import preflight
    preflight(root, sources_dir, {}, mapping["packs"])
    idx = load_index(root)
    from tools.curation.manifests import language_packs
    refs = reference_map(root, language_packs(root))
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
            from tools.curation.links import unlink_missing
            (d / rel).parent.mkdir(parents=True, exist_ok=True)
            (d / rel).write_text(unlink_missing(rewrite_refs("\n".join(parts).rstrip() + "\n", refs, unresolved), d / rel), encoding="utf-8")
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
    print(f"{len(artifacts)} packs, {sum(len(a['supersedes']) for a in artifacts)} upstream items")
    if unresolved:
        print("references to upstream items with no home in the catalog yet:", ", ".join(sorted(unresolved)))


if __name__ == "__main__":
    from tools.curation.__main__ import main
    raise SystemExit(main())
