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
