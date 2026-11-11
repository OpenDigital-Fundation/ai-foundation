"""Synthetic source trees exercise generation without downloading or executing upstream code."""
import shutil
from pathlib import Path

import yaml
import pytest

from tools.curation.bundle import build as build_bundle
from tools.curation.language_pack import build as build_languages

REPO = Path(__file__).resolve().parents[2]


def prepare(tmp_path, domain):
    shutil.copytree(REPO / "catalog", tmp_path / "catalog")
    directory = tmp_path / "domains" / domain
    directory.mkdir(parents=True)
    (directory / "PROVENANCE.yaml").write_text("version: 1\nfiles: []\n")
    sources = tmp_path / "sources"
    clone = sources / "affaan-m_ECC"
    clone.mkdir(parents=True)
    return sources, clone, directory


def test_bundle_normalizes_private_guides_and_records_original_provenance(tmp_path):
    sources, clone, domain = prepare(tmp_path, "testing")
    guide = clone / "synthetic/guide"
    guide.mkdir(parents=True)
    (guide / "SKILL.md").write_text("# Synthetic guide\n\n[Self](SKILL.md)\n")
    registry_before = yaml.safe_load((tmp_path / "catalog/catalog.yaml").read_text())
    build_bundle(tmp_path, sources, {"artifacts": {"testing/browser-testing": {
        "description": "Use when testing the synthetic bundler fixture only.",
        "body": "# Synthetic browser check\n\nUse the guide below.",
        "reference_dirs": {"guide": "affaan-m/ECC:synthetic/guide"},
    }}})
    result = domain / "skills/browser-testing"
    assert (result / "references/guide/README.md").is_file()
    assert "(README.md)" in (result / "references/guide/README.md").read_text()
    files = yaml.safe_load((domain / "PROVENANCE.yaml").read_text())["files"]
    entry = next(f for f in files if f["path"].endswith("guide/README.md"))
    assert entry["derived_from"][0]["path"] == "synthetic/guide/SKILL.md"
    assert yaml.safe_load((tmp_path / "catalog/catalog.yaml").read_text()) == registry_before
    assert not list((tmp_path / "catalog/decisions").rglob("*.yaml"))


def test_language_builder_uses_domain_metadata_without_intermediate_decisions(tmp_path):
    sources, clone, domain = prepare(tmp_path, "languages")
    source = clone / "synthetic/python.md"
    source.parent.mkdir()
    source.write_text("# Synthetic Python standard\n\nPrefer explicit contracts.\n")
    before = (tmp_path / "catalog/catalog.yaml").read_bytes()
    build_languages(tmp_path, sources, {"packs": {"python": {
        "title": "Python", "description": "Use when checking the synthetic Python pack fixture.",
        "topics": {"standards": ["affaan-m/ECC:synthetic/python.md"]},
    }}})
    assert (domain / "skills/python/SKILL.md").is_file()
    assert "explicit contracts" in (domain / "skills/python/references/standards.md").read_text()
    assert (tmp_path / "catalog/catalog.yaml").read_bytes() == before
    assert not list((tmp_path / "catalog/decisions").rglob("*.yaml"))


@pytest.mark.parametrize("builder", ["bundle", "language"])
def test_missing_source_preserves_existing_generated_output(tmp_path, builder):
    domain_name = "testing" if builder == "bundle" else "languages"
    sources, clone, domain = prepare(tmp_path, domain_name)
    output = domain / ("skills/browser-testing" if builder == "bundle" else "skills/python")
    output.mkdir(parents=True)
    sentinel = output / "SKILL.md"
    sentinel.write_text("Existing reviewed content must survive invalid inputs.\n")
    provenance = (domain / "PROVENANCE.yaml").read_bytes()
    registry = (tmp_path / "catalog/catalog.yaml").read_bytes()
    with pytest.raises(ValueError, match="missing source file"):
        if builder == "bundle":
            build_bundle(tmp_path, sources, {"artifacts": {"testing/browser-testing": {
                "description": "Use when exercising the missing source regression.",
                "base": "affaan-m/ECC:missing.md",
            }}})
        else:
            build_languages(tmp_path, sources, {"packs": {"python": {
                "title": "Python", "description": "Use when exercising the missing source regression.",
                "topics": {"standards": ["affaan-m/ECC:missing.md"]},
            }}})
    assert sentinel.read_text() == "Existing reviewed content must survive invalid inputs.\n"
    assert (domain / "PROVENANCE.yaml").read_bytes() == provenance
    assert (tmp_path / "catalog/catalog.yaml").read_bytes() == registry


def test_recipe_cannot_silently_absorb_item_owned_by_another_artifact(tmp_path):
    sources, clone, domain = prepare(tmp_path, "testing")
    import csv
    row = next(row for row in csv.DictReader((tmp_path / "catalog/inventory/artifacts.csv").open())
               if row["source"] == "affaan-m/ECC" and row["kind"] == "skill" and row["name"] == "tdd-workflow")
    source = clone / row["path"]
    source.parent.mkdir(parents=True)
    source.write_text("# Synthetic TDD fixture\n\nOwned by the test-driven-development artifact.\n")
    with pytest.raises(ValueError, match="missing from manifest supersedes"):
        build_bundle(tmp_path, sources, {"artifacts": {"testing/browser-testing": {
            "description": "Use when checking wrong editorial ownership.", "base": "s:tdd-workflow",
        }}})
    assert not (domain / "skills/browser-testing").exists()


def test_cli_preflights_entire_selection_before_starting_any_domain(tmp_path, monkeypatch):
    sources, clone, domain = prepare(tmp_path, "testing")
    from tools.curation.__main__ import main
    sentinel = domain / "skills/browser-testing/SKILL.md"
    sentinel.parent.mkdir(parents=True)
    sentinel.write_text("Existing output\n")
    monkeypatch.chdir(tmp_path)
    before = (tmp_path / "catalog/catalog.yaml").read_bytes()
    with pytest.raises(ValueError, match="missing source"):
        main([str(sources), "--domain", "testing", "--domain", "languages"])
    assert sentinel.read_text() == "Existing output\n"
    assert (tmp_path / "catalog/catalog.yaml").read_bytes() == before


def test_apache_reference_files_carry_modification_notice(tmp_path):
    sources, _, domain = prepare(tmp_path, "testing")
    guide = sources / "getsentry_skills/synthetic/guide"
    (guide / "references").mkdir(parents=True)
    (guide / "SKILL.md").write_text("---\nname: guide\n---\n# Apache guide\n")
    (guide / "references/topic.md").write_text("# Topic\n")
    build_bundle(tmp_path, sources, {"artifacts": {"testing/browser-testing": {
        "description": "Use when testing the Apache notice fixture only.",
        "body": "# Synthetic browser check\n\nUse the guide below.",
        "reference_dirs": {"guide": "getsentry/skills:synthetic/guide"},
    }}})
    refs = domain / "skills/browser-testing/references/guide"
    for f in (refs / "README.md", refs / "references/topic.md"):
        text = f.read_text()
        assert "Modified by OpenDigital from getsentry/skills (Apache-2.0)" in text, f
        assert text.count("Modified by OpenDigital") == 1


def test_notice_covers_assembled_references_and_text_files(tmp_path):
    sources, clone, domain = prepare(tmp_path, "testing")
    (clone / "synthetic").mkdir(parents=True)
    (clone / "synthetic/mit.md").write_text("# MIT part\n\nBody.\n")
    guide = sources / "getsentry_skills/synthetic/guide"
    guide.mkdir(parents=True)
    (guide / "part.md").write_text("# Apache part\n\nBody.\n")
    (guide / "notes.txt").write_text("plain notes\n")
    build_bundle(tmp_path, sources, {"artifacts": {"testing/browser-testing": {
        "description": "Use when testing the Apache notice fixture only.",
        "body": "# Synthetic browser check\n\nUse the guide below.",
        "references": {"mixed.md": ["affaan-m/ECC:synthetic/mit.md", "getsentry/skills:synthetic/guide/part.md"],
                       "mit-only.md": ["affaan-m/ECC:synthetic/mit.md"]},
        "reference_dirs": {"guide": "getsentry/skills:synthetic/guide"},
    }}})
    refs = domain / "skills/browser-testing/references"
    assert "Modified by OpenDigital from getsentry/skills (Apache-2.0)" in (refs / "mixed.md").read_text()
    assert "Modified by OpenDigital" not in (refs / "mit-only.md").read_text()
    assert (refs / "guide/notes.txt").read_text().startswith("Modified by OpenDigital from getsentry/skills (Apache-2.0)")


def test_reference_entry_with_fragment_copies_only_named_sections(tmp_path):
    sources, clone, domain = prepare(tmp_path, "testing")
    (clone / "synthetic").mkdir(parents=True)
    (clone / "synthetic/guide.md").write_text(
        "# Guide\n\nIntro.\n\n## Keep me\n\nKept body.\n\n### Nested detail\n\nAlso kept.\n\n## Drop me\n\nDropped body.\n")
    build_bundle(tmp_path, sources, {"artifacts": {"testing/browser-testing": {
        "description": "Use when testing the section-fragment fixture only.",
        "body": "# Synthetic browser check\n\nSee references.",
        "references": {"derived/extra.md": ["affaan-m/ECC:synthetic/guide.md#keep-me"]},
    }}})
    text = (domain / "skills/browser-testing/references/derived/extra.md").read_text()
    assert "Kept body." in text and "Also kept." in text
    assert "Dropped body." not in text and "Intro." not in text
    files = yaml.safe_load((domain / "PROVENANCE.yaml").read_text())["files"]
    entry = next(f for f in files if f["path"].endswith("derived/extra.md"))
    assert entry["derived_from"][0]["path"] == "synthetic/guide.md#keep-me"
    assert entry["derived_from"][0]["modification"] == "merged-section"


def test_reference_entry_with_missing_fragment_fails_before_writing(tmp_path):
    sources, clone, domain = prepare(tmp_path, "testing")
    (clone / "synthetic").mkdir(parents=True)
    (clone / "synthetic/guide.md").write_text("# Guide\n\n## Only\n\nBody.\n")
    with pytest.raises(ValueError, match="section not found"):
        build_bundle(tmp_path, sources, {"artifacts": {"testing/browser-testing": {
            "description": "Use when testing the section-fragment fixture only.",
            "body": "# Synthetic\n\nBody.",
            "references": {"derived/extra.md": ["affaan-m/ECC:synthetic/guide.md#absent"]},
        }}})
    assert not (domain / "skills/browser-testing").exists()


def test_reference_dir_with_both_skill_and_readme_keeps_the_skill_as_readme(tmp_path):
    sources, clone, domain = prepare(tmp_path, "testing")
    guide = clone / "synthetic/both"
    guide.mkdir(parents=True)
    (guide / "SKILL.md").write_text("# Skill entry\n\nProcedure.\n")
    (guide / "README.md").write_text("# Upstream readme\n\nInstall notes.\n")
    build_bundle(tmp_path, sources, {"artifacts": {"testing/browser-testing": {
        "description": "Use when testing the readme collision fixture only.",
        "body": "# Synthetic\n\nBody.",
        "reference_dirs": {"both": "affaan-m/ECC:synthetic/both"},
    }}})
    readme = domain / "skills/browser-testing/references/both/README.md"
    assert "Procedure." in readme.read_text()
    assert not (readme.parent / "SKILL.md").exists()

def test_reference_install_failure_remains_observable():
    import subprocess
    from tools.curation.language_pack import rewrite_refs
    synthetic = 'npm install example-package@1.2.3 2>/dev/null && echo "upgraded" || echo "not used"'
    adapted = rewrite_refs(synthetic, {}, set())
    shell = 'npm() { printf "synthetic installer failure\\n" >&2; return 42; };\n' + adapted
    result = subprocess.run(["bash", "-c", shell], capture_output=True, text=True)
    assert result.returncode == 42
    assert "synthetic installer failure" in result.stderr
    assert "not used" not in result.stdout


def test_reference_version_selection_is_explicit_and_warnings_survive():
    from tools.curation.language_pack import rewrite_refs
    synthetic = "\n".join([
        "npm install @apollo/client@latest graphql@latest",
        "go get github.com/modelcontextprotocol/go-sdk@latest",
        "COPY --from=composer:latest /usr/bin/composer /usr/bin/composer",
        "image: myapp:latest",
        "Never use @latest in repeatable workflows.",
    ])
    adapted = rewrite_refs(synthetic, {}, set())
    for line in adapted.splitlines():
        if line.startswith(("npm install", "go get", "COPY --from", "image:")):
            assert "latest" not in line
    assert "@apollo/client@<version>" in adapted
    assert "Never use @latest in repeatable workflows." in adapted


@pytest.mark.parametrize("fragment", ["keep", "missing", ""])
def test_import_section_selector_is_validated_before_provenance(tmp_path, fragment):
    from tools.curation.provenance import build as build_provenance
    sources, clone, domain = prepare(tmp_path, "testing")
    (clone / "synthetic").mkdir()
    (clone / "synthetic/guide.md").write_text("# Guide\n\n## Keep\n\nBody.\n")
    dest = domain / "skills/browser-testing/references/derived/guide.md"
    dest.parent.mkdir(parents=True)
    dest.write_text("# Derived\n\nBody.\n")
    mapping = [{"dest": "domains/testing/skills/browser-testing/references/derived/guide.md",
                "source": "affaan-m/ECC", "src": "synthetic/guide.md#" + fragment}]
    if fragment != "keep":
        with pytest.raises(ValueError, match="section"):
            build_provenance(tmp_path, sources, mapping)
    else:
        entry = build_provenance(tmp_path, sources, mapping)["testing"][0]
        assert entry["derived_from"][0]["path"] == "synthetic/guide.md#keep"
        assert entry["derived_from"][0]["modification"] == "merged-section"


def test_markdown_code_heading_is_not_a_document_title():
    from tools.curation.language_pack import body_of, pick_sections
    raw = "---\nname: example\n---\n```python\n# Preserve this code comment\nprint(1)\n```\n\n## Keep\n\nText.\n"
    title, body = body_of(raw)
    assert title == "example"
    assert "# Preserve this code comment" in body
    selected = pick_sections(raw, ["keep"])
    assert "# Preserve this code comment" not in selected
    assert "Text." in selected


@pytest.mark.parametrize("suffix,header,licence", [
    (".bst", "% This file may be distributed under the conditions of the LaTeX Project Public License,\n% either version 1.3 of this license or any later version.\n", "LPPL-1.3"),
    (".tex", "%% This file may be redistributed under the conditions of the\n%% LaTeX Project Public License, either version 1.3c or later.\n", "LPPL-1.3c"),
    (".py", "# SPDX-License-Identifier: GPL-3.0-only\n", "GPL-3.0-only"),
    (".md", "SPDX-License-Identifier: MIT AND GPL-3.0-only\n", "Restricted"),
])
def test_file_license_header_overrides_permissive_collection(tmp_path, suffix, header, licence):
    from tools.curation.licences import check_copy, effective_licence
    sources = tmp_path / "sources"
    clone = sources / "synthetic_collection"
    clone.mkdir(parents=True)
    (clone / "asset" ).with_suffix(suffix).write_text(header + "Synthetic fixture.\n")
    lock = {"synthetic/collection": {"license": "MIT"}}
    path = "asset" + suffix
    assert effective_licence(lock, sources, "synthetic/collection", path).startswith(licence)
    with pytest.raises(ValueError, match="does not permit copying"):
        check_copy(lock, sources, "synthetic/collection", path)


def test_reference_omission_is_exact_reproducible_and_prunes_only_its_provenance(tmp_path):
    sources, clone, domain = prepare(tmp_path, "testing")
    guide = clone / "synthetic/guide"
    guide.mkdir(parents=True)
    restricted = "% This file may be distributed under the LaTeX Project Public License, version 1.3.\n"
    (guide / "blocked.tex").write_text(restricted)
    (guide / "allowed.md").write_text("# Allowed fixture\n")
    output = domain / "skills/browser-testing"
    output.mkdir(parents=True)
    sentinel = output / "SKILL.md"
    sentinel.write_text("Existing reviewed output\n")
    unrelated = {"path": "skills/another/old.md", "derived_from": []}
    old = {"path": "skills/browser-testing/references/guide/blocked.tex", "derived_from": []}
    (domain / "PROVENANCE.yaml").write_text(yaml.safe_dump({"version": 1, "files": [old, unrelated]}))
    recipe = {"description": "Use when testing exact reference omissions.", "body": "# Fixture\n",
              "reference_dirs": {"guide": "affaan-m/ECC:synthetic/guide"}}
    spec = {"artifacts": {"testing/browser-testing": recipe}}
    before = (domain / "PROVENANCE.yaml").read_bytes()
    with pytest.raises(ValueError, match="LPPL"):
        build_bundle(tmp_path, sources, spec)
    assert sentinel.read_text() == "Existing reviewed output\n"
    assert (domain / "PROVENANCE.yaml").read_bytes() == before
    recipe["reference_excludes"] = {"guide": ["blocked.tex"]}
    build_bundle(tmp_path, sources, spec)
    assert not (output / "references/guide/blocked.tex").exists()
    assert (output / "references/guide/allowed.md").is_file()
    assert (guide / "blocked.tex").read_text() == restricted
    files = yaml.safe_load((domain / "PROVENANCE.yaml").read_text())["files"]
    assert unrelated in files and old not in files
    first = {str(p.relative_to(domain)): p.read_bytes() for p in domain.rglob("*") if p.is_file()}
    build_bundle(tmp_path, sources, spec)
    assert {str(p.relative_to(domain)): p.read_bytes() for p in domain.rglob("*") if p.is_file()} == first


@pytest.mark.parametrize("directory,excluded", [("guide", "../escape"), ("guide", "missing.tex"),
                                                  ("guide", "nested"), ("unknown", "allowed.md")])
def test_invalid_reference_omission_fails_before_mutation(tmp_path, directory, excluded):
    sources, clone, domain = prepare(tmp_path, "testing")
    guide = clone / "synthetic/guide"
    (guide / "nested").mkdir(parents=True)
    (guide / "allowed.md").write_text("# Allowed\n")
    before = (domain / "PROVENANCE.yaml").read_bytes()
    with pytest.raises(ValueError):
        build_bundle(tmp_path, sources, {"artifacts": {"testing/browser-testing": {
            "description": "Use when testing invalid omissions.", "body": "# Fixture\n",
            "reference_dirs": {"guide": "affaan-m/ECC:synthetic/guide"},
            "reference_excludes": {directory: [excluded]},
        }}})
    assert not (domain / "skills/browser-testing").exists()
    assert (domain / "PROVENANCE.yaml").read_bytes() == before


@pytest.mark.parametrize("fragment", ["", "keep,", ",keep"])
def test_assembled_reference_rejects_empty_selector(tmp_path, fragment):
    from tools.curation.language_pack import section
    source = tmp_path / "fixture_source"
    source.mkdir()
    (source / "guide.md").write_text("# Guide\n\n## Keep\n\nBody.\n")
    with pytest.raises(ValueError, match="selector"):
        section(tmp_path, "fixture/source", "guide.md#" + fragment, {"fixture/source": {"commit": "1234567", "license": "MIT"}})


def test_section_selection_can_name_parent_and_child():
    from tools.curation.language_pack import pick_sections
    selected = pick_sections("# Guide\n\n## Parent\n\nBody.\n\n### Child\n\nDetail.\n\n## Other\n\nDrop.\n", ["parent", "child"])
    assert "Body." in selected and "Detail." in selected and "Drop." not in selected


def test_science_template_index_lists_only_bundled_assets():
    # Parse metadata as data: never import or execute the upstream reference script.
    import ast
    directory = REPO / "domains/science/skills/scientific-writing/references/venue-templates"
    tree = ast.parse((directory / "scripts/query_template.py").read_text())
    declaration = next(node for node in tree.body if isinstance(node, ast.Assign)
                       and any(isinstance(target, ast.Name) and target.id == "TEMPLATES" for target in node.targets))
    templates = ast.literal_eval(declaration.value)
    for category, entries in templates.items():
        for name, metadata in entries.items():
            assert (directory / "assets" / category / metadata["file"]).is_file(), name
    assert not any(name.startswith("elsevier-") for name in templates["journals"])


def test_reference_override_uses_final_canonical_path(tmp_path):
    sources, clone, domain = prepare(tmp_path, "testing")
    guide = clone / "synthetic/guide"
    guide.mkdir(parents=True)
    (guide / "SKILL.md").write_text("# Upstream guide\n\nOriginal body.\n")
    override = tmp_path / "catalog/overrides/testing/browser-testing/references/guide/README.md"
    override.parent.mkdir(parents=True)
    override.write_text("# Reviewed guide\n\nLocally adapted body.\n")
    build_bundle(tmp_path, sources, {"artifacts": {"testing/browser-testing": {
        "description": "Use when testing canonical reference overrides.", "body": "# Fixture\n",
        "reference_dirs": {"guide": "affaan-m/ECC:synthetic/guide"},
    }}})
    output = domain / "skills/browser-testing/references/guide"
    assert (output / "README.md").read_text() == override.read_text()
    assert not (output / "SKILL.md").exists()
    files = yaml.safe_load((domain / "PROVENANCE.yaml").read_text())["files"]
    entry = next(f for f in files if f["path"].endswith("guide/README.md"))
    assert entry["derived_from"][0]["path"] == "synthetic/guide/SKILL.md"
