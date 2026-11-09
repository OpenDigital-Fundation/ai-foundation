from pathlib import Path

from tools.inventory.build import classify_licence_text, is_permissive, licence_of, same_licence


def test_classify_common_licences():
    assert classify_licence_text("MIT License\n\nPermission is hereby granted, free of charge") == "MIT"
    assert classify_licence_text("                 Apache License\n Version 2.0") == "Apache-2.0"
    assert classify_licence_text("Modified MIT License\nPermission is hereby granted, free of charge").startswith("Restricted")
    assert classify_licence_text("Attribution-ShareAlike 4.0 International") == "CC-BY-SA-4.0"
    assert classify_licence_text("Use of these Figma skills is subject to the Figma terms").startswith("Restricted")


def test_nearest_skill_licence_overrides_source_licence(tmp_path: Path):
    src = tmp_path / "src"
    (src / "skills/free").mkdir(parents=True)
    (src / "skills/closed").mkdir(parents=True)
    (src / "skills/closed/LICENSE.txt").write_text("Copyright 2025 Example Inc. All rights reserved.")
    (src / "skills/free/LICENSE").write_text("Apache License Version 2.0")
    source = {"id": "x/y", "license": "NOASSERTION"}
    assert licence_of(source, "skills/free/SKILL.md", "free", src) == "Apache-2.0"
    assert not is_permissive(licence_of(source, "skills/closed/SKILL.md", "closed", src))
    assert licence_of(source, "README.md", "", src) == "NOASSERTION"


def test_same_licence_normalises_labels():
    assert same_licence("Restricted (Modified MIT)", "Modified-MIT (no AI training/evaluation use)")
    assert not same_licence("Restricted (see LICENSE)", "Apache-2.0")


def test_copilot_instructions_are_rules():
    from tools.inventory.build import kind_of
    assert kind_of("github/awesome-copilot", "instructions/python.instructions.md", "python.instructions.md") == "rule"
    assert kind_of("github/awesome-copilot", "agents/x.agent.md", "x.agent.md") == "agent"
    assert kind_of("github/awesome-copilot", "README.md", "README.md") is None


def test_copilot_generic_json_names_use_their_folder():
    from tools.inventory.build import artifact_name, kind_of
    assert kind_of("github/awesome-copilot", "plugins/go-mcp-development/plugin.json", "plugin.json") is None
    assert artifact_name("github/awesome-copilot", "hooks/dependency-check/hooks.json", "hook") == "dependency-check"
    assert artifact_name("github/awesome-copilot", "plugins/awesome-copilot/mcp.json", "mcp") == "awesome-copilot"
    assert artifact_name("github/awesome-copilot", "mcp.json", "mcp") == "mcp"
    # other sources keep their established keys
    assert artifact_name("trailofbits/skills", "plugins/gh-cli/hooks/hooks.json", "hook") == "hooks"
