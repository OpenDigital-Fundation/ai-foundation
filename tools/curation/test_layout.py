from pathlib import Path

import pytest

from tools.curation.layout import normalize, remap_provenance, upstream_path
from tools.validate.checks import check_support_layout


def test_normalize_preserves_assets_and_relinks_reference_entries(tmp_path):
    art = tmp_path / "domains/ui/skills/example"
    guide = art / "references/guide"
    guide.mkdir(parents=True)
    fonts = art / "canvas-fonts"
    fonts.mkdir()
    (fonts / "font.ttf").write_bytes(b"synthetic-font-data\x00\xff")
    (guide / "SKILL.md").write_text("# Guide\n\n[This guide](SKILL.md)\n")
    (art / "SKILL.md").write_text("# Entry\n\n[Guide](references/guide/SKILL.md)\nUse `./canvas-fonts`.\n")
    provenance = [{"path": "skills/example/references/guide/SKILL.md", "derived_from": [{"path": "upstream/SKILL.md"}]}]
    moves = normalize(art)
    remap_provenance(provenance, "skills/example", moves)
    assert (art / "SKILL.md").read_text() == "# Entry\n\n[Guide](references/guide/README.md)\nUse `./assets/fonts`.\n"
    assert "(README.md)" in (guide / "README.md").read_text()
    assert (art / "assets/fonts/font.ttf").read_bytes() == b"synthetic-font-data\x00\xff"
    assert provenance[0]["path"].endswith("/README.md")
    assert provenance[0]["derived_from"][0]["path"] == "upstream/SKILL.md"
    assert normalize(art) == {}
    assert check_support_layout(tmp_path) == []


def test_normalize_rejects_collision_before_moving_any_file(tmp_path):
    reference = tmp_path / "references/example"
    reference.mkdir(parents=True)
    (reference / "SKILL.md").write_text("original")
    (reference / "README.md").write_text("independent existing guide")
    with pytest.raises(ValueError, match="collision"):
        normalize(tmp_path)
    assert (reference / "SKILL.md").read_text() == "original"
    assert (reference / "README.md").read_text() == "independent existing guide"


def test_provenance_lookup_keeps_upstream_names(tmp_path):
    (tmp_path / "references").mkdir()
    (tmp_path / "references/SKILL.md").write_text("original")
    (tmp_path / "canvas-fonts").mkdir()
    (tmp_path / "canvas-fonts/font.ttf").write_bytes(b"font")
    assert upstream_path(tmp_path, "references/README.md") == "references/SKILL.md"
    assert upstream_path(tmp_path, "assets/fonts/font.ttf") == "canvas-fonts/font.ttf"


def test_validator_rejects_nested_skill_entry(tmp_path):
    reference = tmp_path / "domains/testing/skills/check/references/guide"
    reference.mkdir(parents=True)
    (reference / "SKILL.md").write_text("nested")
    assert any("references use README.md" in e for e in check_support_layout(tmp_path))
