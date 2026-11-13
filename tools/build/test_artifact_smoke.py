import json
from pathlib import Path
import zipfile

import pytest

from tools.build.artifact_smoke import ROOTS, pack, sha256, verify


@pytest.fixture
def bundle(tmp_path):
    adapters = tmp_path / "adapters"
    for name, prefix in ROOTS.items():
        skill = adapters.joinpath(*prefix, "example")
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("# Synthetic example\n")
        hidden = skill / "assets/.claude-plugin/plugin.json"
        hidden.parent.mkdir(parents=True); hidden.write_text('{}\n')
    output = tmp_path / "packages"
    pack(adapters, output, 1)
    return output


def test_four_package_roundtrip_preserves_hidden_runtime_assets(bundle):
    assert verify(bundle) == {"packages": 4, "skills": {name: 1 for name in ROOTS}, "hashes_verified": True}
    for name in ROOTS:
        with zipfile.ZipFile(bundle / f"ai-foundation-{name}.zip") as archive:
            assert any(n.endswith('/assets/.claude-plugin/plugin.json') for n in archive.namelist())


def test_changed_bytes_fail_integrity_check(bundle):
    archive = bundle / "ai-foundation-agent-skills.zip"
    with archive.open('ab') as target: target.write(b'changed')
    with pytest.raises(ValueError, match="hash mismatch"): verify(bundle)


def test_missing_archive_is_not_a_success(bundle):
    archive = bundle / "ai-foundation-gemini.zip"; archive.rename(archive.with_suffix('.saved'))
    with pytest.raises(ValueError, match="missing package"): verify(bundle)


def test_traversal_is_rejected_even_with_a_matching_hash(bundle):
    archive = bundle / "ai-foundation-agent-skills.zip"
    with zipfile.ZipFile(archive, 'a') as target: target.writestr('../escape.txt','synthetic')
    manifest_path = bundle / "manifest.json"; manifest = json.loads(manifest_path.read_text())
    manifest['packages']['agent-skills']['sha256'] = sha256(archive); manifest_path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="ZIP path"): verify(bundle)
    assert not (bundle.parent/'escape.txt').exists()


def test_wrong_public_entry_count_fails(bundle):
    manifest_path = bundle / "manifest.json"; manifest = json.loads(manifest_path.read_text())
    manifest['expected_skills'] = 2; manifest_path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="count mismatch"): verify(bundle)


def test_pack_never_overwrites_existing_output(bundle):
    with pytest.raises(ValueError, match="new directory"): pack(bundle.parent/'adapters',bundle,1)
    assert verify(bundle)['packages'] == 4
