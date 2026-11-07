import json
import tomllib
from pathlib import Path

import yaml

from tools.build.adapters import build_all

REPO = Path(__file__).resolve().parents[2]


def test_adapters_project_every_skill(tmp_path):
    result = build_all(REPO, tmp_path / "dist")
    n = result["skills"]
    out = tmp_path / "dist"
    assert n > 0
    # Agent Skills layout: one directory per skill with a SKILL.md and no evals
    skills = sorted((out / "agent-skills").iterdir())
    assert len(skills) == n and all((s / "SKILL.md").is_file() and not (s / "evals").exists() for s in skills)
    # Cursor: valid frontmatter, principles always applied, links resolve to the installed skill
    rules = sorted((out / "cursor/.cursor/rules").glob("*.mdc"))
    assert len(rules) == n
    for r in rules:
        text = r.read_text()
        fm = yaml.safe_load(text.split("---\n")[1])
        assert fm["description"].startswith("Use ") and isinstance(fm["alwaysApply"], bool)
        for link in __import__("re").findall(r"\]\((\.\./\.\./\.agents/skills/[^)#\s]+)", text):
            assert (r.parent / link).resolve().exists(), (r.name, link)
    assert yaml.safe_load((out / "cursor/.cursor/rules/coding-discipline.mdc").read_text().split("---\n")[1])["alwaysApply"] is True
    # Gemini: manifest, context file and one parseable command per skill
    assert json.loads((out / "gemini/gemini-extension.json").read_text())["contextFileName"] == "GEMINI.md"
    commands = list((out / "gemini/commands").rglob("*.toml"))
    assert len(commands) == n
    for c in commands:
        data = tomllib.loads(c.read_text())
        assert data["description"] and "{{args}}" in data["prompt"]
    # OpenCode: skills plus an index
    assert len(list((out / "opencode/.opencode/skills").iterdir())) == n
    assert "code-quality/agents/code-reviewer.md" in (out / "opencode/AGENTS.md").read_text()
