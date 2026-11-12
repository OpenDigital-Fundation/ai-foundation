import json
import tomllib
from pathlib import Path

import yaml

from tools.build.adapters import build_all, build_agent_skills
from tools.validate.repo import discover

import pytest

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
    descriptions = {a.name: a.frontmatter["description"] for a in discover(REPO) if a.type in {"skill", "workflow"}}
    for r in rules:
        text = r.read_text()
        fm = yaml.safe_load(text.split("---\n")[1])
        assert fm["description"] == descriptions[r.stem] and isinstance(fm["alwaysApply"], bool)
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


def test_registered_shared_knowledge_is_local_with_fragment_and_origin(tmp_path):
    root = tmp_path / "repo"
    skill = root / "domains/example/skills/read-guide"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: read-guide\ndescription: Read the shared guide for this bounded example task.\n---\n[Guide](../../knowledge/shared.md#section)\n")
    knowledge = root / "domains/example/knowledge/shared.md"
    knowledge.parent.mkdir(); knowledge.write_text("# Shared\n\n## Section\nOriginal local guidance.\n")
    out = tmp_path / "package"
    build_agent_skills(root, out, [{"dir": skill, "name": "read-guide"}])
    entry = (out / "read-guide/SKILL.md").read_text()
    assert "references/catalog-support/example/knowledge/shared.md#section" in entry
    assert (out / "read-guide/references/catalog-support/example/knowledge/shared.md").read_text() == knowledge.read_text()
    origins = json.loads((out / "read-guide/references/catalog-support/origins.json").read_text())
    assert list(origins.values()) == ["domains/example/knowledge/shared.md"]


def test_adapter_refuses_unregistered_repository_file(tmp_path):
    root = tmp_path / "repo"
    skill = root / "domains/example/skills/unsafe-reference"
    skill.mkdir(parents=True)
    (root / "private.txt").write_text("not a public catalog resource")
    (skill / "SKILL.md").write_text("[Private](../../../../private.txt)\n")
    with pytest.raises(ValueError, match="not registered public support"):
        build_agent_skills(root, tmp_path / "package", [{"dir": skill, "name": "unsafe-reference"}])
    assert not list((tmp_path / "package").rglob("private.txt"))


def test_literal_markdown_example_is_not_treated_as_a_resource(tmp_path):
    root = tmp_path / "repo"
    skill = root / "domains/example/skills/literal-example"
    skill.mkdir(parents=True)
    sample = "Write a link as `[label](url)`; this is syntax, not a file.\n"
    (skill / "SKILL.md").write_text(sample)
    build_agent_skills(root, tmp_path / "package", [{"dir": skill, "name": "literal-example"}])
    assert (tmp_path / "package/literal-example/SKILL.md").read_text() == sample
