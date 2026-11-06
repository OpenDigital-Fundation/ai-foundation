import shutil
from pathlib import Path

import pytest
import yaml

from tools.validate.checks import run_all

REPO = Path(__file__).resolve().parents[2]

TDD = ("Use when implementing any feature or bugfix, before writing implementation code. "
       "Write a failing test first, watch it fail, write minimal code to pass, then refactor.")
TDD_PARAPHRASE = ("Use when implementing a feature or a bugfix, before writing any implementation code: "
                  "write the failing test first, watch it fail, write the minimal code to pass, refactor.")


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A minimal repository: the real catalog contracts and domain manifests, but no content."""
    shutil.copytree(REPO / "catalog", tmp_path / "catalog", ignore=shutil.ignore_patterns("decisions"))
    (tmp_path / "catalog/catalog.yaml").write_text("version: 1\nartifacts: []\n")
    (tmp_path / "catalog/exclusions.yaml").write_text("version: 1\nexcluded: []\n")
    for manifest in (REPO / "domains").glob("*/.claude-plugin/plugin.json"):
        d = tmp_path / "domains" / manifest.parent.parent.name
        (d / ".claude-plugin").mkdir(parents=True)
        shutil.copy(manifest, d / ".claude-plugin/plugin.json")
        (d / "PROVENANCE.yaml").write_text("version: 1\nfiles: []\n")
    (tmp_path / "tools/inventory").mkdir(parents=True)
    return tmp_path


def add_skill(root: Path, domain: str, name: str, description: str, status: str = "experimental", register: bool = True):
    d = root / "domains" / domain / "skills" / name
    d.mkdir(parents=True)
    fm = yaml.safe_dump({"name": name, "description": description}, sort_keys=False, width=1000)
    (d / "SKILL.md").write_text(f"---\n{fm}---\n\n# {name}\n\nBody.\n")
    if register:
        cat = yaml.safe_load((root / "catalog/catalog.yaml").read_text())
        cat["artifacts"].append({"id": f"{domain}/{name}", "type": "skill", "capability": description[:150],
                                 "status": status, "owner": "@opendigital/ai-foundation"})
        (root / "catalog/catalog.yaml").write_text(yaml.safe_dump(cat, sort_keys=False))
    return d


def errors(root: Path) -> list[str]:
    return run_all(root)[0]


def test_clean_repo_passes():
    errs, _ = run_all(REPO)
    assert errs == []


def test_valid_skill_passes(repo):
    add_skill(repo, "testing", "test-driven-development", TDD)
    assert errors(repo) == []


def test_branded_cross_domain_name_is_rejected(repo):
    add_skill(repo, "ui", "ui-ux-pro-max", "Use when designing interfaces of any kind: styles, palettes, fonts and UX guidelines.")
    errs = errors(repo)
    assert any("forbidden term" in e and "ui-ux-pro-max" in e for e in errs)


def test_paraphrased_duplicate_is_rejected(repo):
    add_skill(repo, "testing", "test-driven-development", TDD)
    add_skill(repo, "testing", "red-green-refactor", TDD_PARAPHRASE)
    assert any("overlapping triggers" in e for e in errors(repo))


def test_distinct_skills_do_not_collide(repo):
    add_skill(repo, "testing", "test-driven-development", TDD)
    add_skill(repo, "debugging", "systematic-debugging",
              "Use when encountering a bug, test failure or unexpected behaviour, before proposing fixes. Find the root cause first.")
    assert errors(repo) == []


def test_unregistered_artifact_and_orphan_entry(repo):
    add_skill(repo, "testing", "test-driven-development", TDD, register=False)
    cat = yaml.safe_load((repo / "catalog/catalog.yaml").read_text())
    cat["artifacts"].append({"id": "testing/ghost-skill", "type": "skill", "capability": "Does not exist on disk at all.",
                             "status": "experimental", "owner": "x"})
    (repo / "catalog/catalog.yaml").write_text(yaml.safe_dump(cat))
    errs = errors(repo)
    assert any("is not registered" in e for e in errs)
    assert any("ghost-skill' has no file" in e for e in errs)


def test_name_must_match_directory(repo):
    d = add_skill(repo, "testing", "test-driven-development", TDD)
    (d / "SKILL.md").write_text(f"---\nname: tdd\ndescription: {TDD}\n---\nBody\n")
    assert any("must equal 'test-driven-development'" in e for e in errors(repo))


def test_copy_of_restricted_file_is_rejected(repo):
    d = add_skill(repo, "documents", "office-documents", "Use when a task needs Word, Excel, PowerPoint or PDF files as input or output.")
    restricted = d / "references" / "docx.md"
    restricted.parent.mkdir()
    restricted.write_text("© 2025 Anthropic, PBC. All rights reserved. " * 5)
    import hashlib
    h = hashlib.sha256(restricted.read_bytes()).hexdigest()
    (repo / "tools/inventory/reference-hashes.txt").write_text(f"{h} anthropics/skills:skills/docx/SKILL.md\n")
    assert any("restricted-licence" in e for e in errors(repo))


def test_provenance_from_reference_only_source_is_rejected(repo):
    add_skill(repo, "security", "penetration-testing", "Use when asked to run an authorised penetration test against a web application or API.")
    (repo / "domains/security/PROVENANCE.yaml").write_text(yaml.safe_dump({"version": 1, "files": [{
        "path": "skills/penetration-testing/SKILL.md",
        "derived_from": [{"source": "SecurityStandards/agent-pentester", "commit": "2468b67", "path": "README.md",
                          "license": "AGPL-3.0", "modification": "adapted"}]}]}))
    assert any("reference-only source" in e for e in errors(repo))


def test_stable_requires_evals(repo):
    d = add_skill(repo, "testing", "test-driven-development", TDD, status="stable")
    assert any("requires evals/triggers.yaml" in e for e in errors(repo))
    (d / "evals").mkdir()
    (d / "evals/triggers.yaml").write_text("should_trigger: []\n")
    (d / "evals/tasks.yaml").write_text("[]\n")
    assert errors(repo) == []


def test_skill_line_budget(repo):
    d = add_skill(repo, "testing", "test-driven-development", TDD)
    (d / "SKILL.md").write_text(f"---\nname: test-driven-development\ndescription: {TDD}\n---\n" + "line\n" * 501)
    assert any("exceeds 500" in e for e in errors(repo))


def test_unpinned_mcp_is_rejected(repo):
    m = repo / "domains/platform/mcps"
    m.mkdir()
    (m / "github.json").write_text('{"mcpServers": {"github": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-github"]}}}')
    assert any("pinned to an exact version" in e for e in errors(repo))
    (m / "github.json").write_text('{"mcpServers": {"github": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-github@2025.4.8"]}}}')
    assert errors(repo) == [] or not any("pinned" in e for e in errors(repo))


def test_hygiene_flags_absolute_paths_and_forced_activation(repo):
    d = add_skill(repo, "testing", "test-driven-development", TDD)
    (d / "SKILL.md").write_text(f"---\nname: test-driven-development\ndescription: {TDD}\n---\n"
                                "Read /Users/alice/notes.md. You MUST use this skill before ANY response.\n")
    errs = errors(repo)
    assert any("absolute machine path" in e for e in errs)
    assert any("self-promoting" in e for e in errs)


def test_line_budget_exception_needs_a_reason(repo):
    d = add_skill(repo, "testing", "test-driven-development", TDD)
    long_body = "line\n" * 501
    (d / "SKILL.md").write_text(f"---\nname: test-driven-development\ndescription: {TDD}\nmetadata:\n  line_budget_exception: short\n---\n" + long_body)
    assert any("exceeds 500" in e for e in errors(repo))
    (d / "SKILL.md").write_text(f"---\nname: test-driven-development\ndescription: {TDD}\nmetadata:\n  line_budget_exception: Upstream official skill whose relative links break if split.\n---\n" + long_body)
    assert not any("exceeds 500" in e for e in errors(repo))
