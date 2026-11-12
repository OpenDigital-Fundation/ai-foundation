"""Project the catalog onto other harnesses. Output goes to dist/<harness>/ and is never committed.

python -m tools.build adapters [out-dir]     (default: dist)

- agent-skills/  Agent Skills layout (Codex, Copilot CLI, Gemini CLI, OpenCode read ~/.agents/skills/)
- cursor/        .cursor/rules/<name>.mdc that point at the installed skill files
- gemini/        a Gemini CLI extension: gemini-extension.json, GEMINI.md and one command per skill
- opencode/      skills plus an AGENTS.md index for OpenCode
Only skills and workflows are projected; Claude Code subagents are listed in each index for harnesses
without a subagent format.
"""
from __future__ import annotations

import json
import os
import re
import shutil
from pathlib import Path

import yaml

from tools.validate.repo import discover, parse_frontmatter


def _entries(root: Path) -> list[dict]:
    status = {a["id"]: a["status"] for a in yaml.safe_load((root / "catalog/catalog.yaml").read_text())["artifacts"]}
    out = []
    for a in discover(root):
        if a.type in {"skill", "workflow"} and status.get(a.id) != "deprecated":
            out.append({"id": a.id, "domain": a.domain, "name": a.name, "dir": a.path.parent,
                        "description": str(a.frontmatter["description"]), "body": a.body, "status": status.get(a.id)})
    return sorted(out, key=lambda e: e["id"])


def _agents(root: Path) -> list[str]:
    return sorted(f"{p.parent.parent.name}:{p.stem}" for p in root.glob("domains/*/agents/*.md"))


def build_agent_skills(root: Path, out: Path, entries: list[dict]) -> None:
    support = {a.path.resolve() for a in discover(root)
               if a.type in {"knowledge", "agent", "template"} and a.path.is_file()}
    for e in entries:
        dest = out / e["name"]
        shutil.copytree(e["dir"], dest, ignore=shutil.ignore_patterns("evals"))
        _portable_links(root, e["dir"], dest, support)


def _portable_links(root: Path, source: Path, dest: Path, support: set[Path]) -> None:
    """Keep registered public support local to a flat skill, never copy arbitrary paths."""
    source, dest = source.resolve(), dest.resolve()
    domains = (root / "domains").resolve()
    pending = [(source / p.relative_to(dest), p) for p in sorted(dest.rglob("*.md"))]
    copied: dict[Path, Path] = {}
    link = re.compile(r"(?P<head>\]\()(?P<target>(?!https?://|#|mailto:|/)[^)\s]+)(?P<tail>\))")
    while pending:
        src, projected = pending.pop()

        def replace(match):
            path, marker, fragment = match["target"].partition("#")
            target = (src.parent / path).resolve()
            if target.is_relative_to(source):
                local = dest / target.relative_to(source)
                if not local.exists():
                    raise ValueError(f"{src}: reference excluded from package: {path}")
            else:
                if target not in support or not target.is_relative_to(domains):
                    raise ValueError(f"{src}: reference is not registered public support: {path}")
                local = copied.get(target)
                if local is None:
                    local = dest / "references/catalog-support" / target.relative_to(domains)
                    if local.exists():
                        raise ValueError(f"reserved adapter support destination already exists: {local}")
                    local.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(target, local)
                    copied[target] = local
                    if target.suffix == ".md":
                        pending.append((target, local))
            rel = Path(os.path.relpath(local, projected.parent)).as_posix()
            return match["head"] + rel + (marker + fragment if marker else "") + match["tail"]

        original = projected.read_text()
        parts = re.split(r"(?ms)(^```.*?^```|^~~~.*?^~~~)", original)
        def prose(part):
            spans = re.split(r"(`[^`\n]*`)", part)
            return "".join(span if n % 2 else link.sub(replace, span) for n, span in enumerate(spans))
        rewritten = "".join(part if i % 2 else prose(part) for i, part in enumerate(parts))
        if rewritten != original:
            projected.write_text(rewritten)
    if copied:
        origins = {p.relative_to(dest).as_posix(): s.relative_to(root.resolve()).as_posix()
                   for s, p in sorted(copied.items())}
        (dest / "references/catalog-support/origins.json").write_text(json.dumps(origins, indent=2) + "\n")


def _relink(text: str, prefix: str) -> str:
    """Prefix relative links outside fenced code blocks."""
    parts = re.split(r"(?ms)(^```.*?^```|^~~~.*?^~~~)", text)
    link = re.compile(r"\]\((?!https?://|#|mailto:|/)([^)\s]+)\)")
    return "".join(p if i % 2 else link.sub(lambda m: f"]({prefix}{m.group(1)})", p) for i, p in enumerate(parts))


def build_cursor(root: Path, out: Path, entries: list[dict]) -> None:
    rules = out / ".cursor/rules"
    rules.mkdir(parents=True)
    build_agent_skills(root, out / ".agents/skills", entries)
    for e in entries:
        always = e["domain"] == "principles"
        head = {"description": e["description"], "globs": "", "alwaysApply": always}
        projected = out / ".agents/skills" / e["name"] / "SKILL.md"
        _, projected_body = parse_frontmatter(projected.read_text())
        body = (f"# {e['name']}\n\nThis rule mirrors the `{e['id']}` skill. Its references and scripts are installed at "
                f"`~/.agents/skills/{e['name']}/` (or the project's `.agents/skills/{e['name']}/`); open them when the steps below say so.\n\n"
                + _relink(projected_body.strip(), f"../../.agents/skills/{e['name']}/") + "\n")
        (rules / f"{e['name']}.mdc").write_text("---\n" + yaml.safe_dump(head, sort_keys=False, width=1000) + "---\n" + body)


def build_gemini(root: Path, out: Path, entries: list[dict]) -> None:
    out.mkdir(parents=True)
    (out / "gemini-extension.json").write_text(json.dumps({"name": "opendigital-ai-foundation", "version": "0.0.0",
                                                            "contextFileName": "GEMINI.md"}, indent=2) + "\n")
    build_agent_skills(root, out / "skills", entries)
    lines = ["# OpenDigital AI Foundation", "", "Skills live in `skills/<name>/SKILL.md` inside this extension. "
             "When a task matches a description below, read that SKILL.md and follow it; load its references only when it says so.", ""]
    lines += [f"- **{e['name']}** ({e['domain']}): {e['description']}" for e in entries]
    (out / "GEMINI.md").write_text("\n".join(lines) + "\n")
    for e in entries:
        d = out / "commands" / e["domain"]
        d.mkdir(parents=True, exist_ok=True)
        prompt = (f"Read the skill file skills/{e['name']}/SKILL.md in this extension and follow it for this request: {{{{args}}}}")
        # JSON string escapes are valid TOML basic-string escapes
        (d / f"{e['name']}.toml").write_text(f"description = {json.dumps(e['description'])}\nprompt = {json.dumps(prompt)}\n")


def build_opencode(root: Path, out: Path, entries: list[dict]) -> None:
    build_agent_skills(root, out / ".opencode/skills", entries)
    lines = ["# OpenDigital AI Foundation skills", "", "Read `.opencode/skills/<name>/SKILL.md` when a task matches:", ""]
    lines += [f"- `{e['name']}` — {e['description']}" for e in entries]
    agents = _agents(root)
    if agents:
        lines += ["", "Subagent prompts (use as a fresh-context helper if your harness supports it): "
                  + ", ".join(f"`domains/{a.split(':')[0]}/agents/{a.split(':')[1]}.md`" for a in agents)]
    (out / "AGENTS.md").write_text("\n".join(lines) + "\n")


def build_all(root: Path, out: Path) -> dict[str, int]:
    if out.exists():
        shutil.rmtree(out)  # generated output directory owned by this tool
    entries = _entries(root)
    names = [e["name"] for e in entries]
    if len(names) != len(set(names)):
        raise SystemExit("skill names must be unique to project onto flat harness layouts")
    build_agent_skills(root, out / "agent-skills", entries)
    build_cursor(root, out / "cursor", entries)
    build_gemini(root, out / "gemini", entries)
    build_opencode(root, out / "opencode", entries)
    return {"skills": len(entries)}
