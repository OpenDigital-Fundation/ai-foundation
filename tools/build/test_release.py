import json
from pathlib import Path
import subprocess
import zipfile

import pytest
import yaml

from tools.build import release
from tools.build.release_verify import TARGETS, sha256, verify

COMMIT = 'a' * 40


@pytest.fixture
def source(tmp_path):
    root = tmp_path / 'source'
    (root / 'catalog').mkdir(parents=True)
    artifacts = []
    for name, kind in [('first', 'skill'), ('second', 'workflow')]:
        skill = root / f'domains/example/{kind}s/{name}'
        skill.mkdir(parents=True)
        (skill / 'SKILL.md').write_text(f'---\nname: {name}\ndescription: Use for the {name} synthetic task.\n---\n[Shared](../../knowledge/shared.md#section)\n')
        hidden = skill / 'assets/.claude-plugin/plugin.json'
        hidden.parent.mkdir(parents=True); hidden.write_text('{}\n')
        artifacts.append({'id': f'example/{name}', 'type': kind, 'status': 'experimental'})
    shared = root / 'domains/example/knowledge/shared.md'
    shared.parent.mkdir(parents=True); shared.write_text('# Shared\n\n## Section\nSynthetic support.\n')
    (root / 'domains/example/PROVENANCE.yaml').write_text('version: 1\nartifacts: []\n')
    (root / 'catalog/catalog.yaml').write_text(yaml.safe_dump({'artifacts': artifacts}))
    (root / '.claude-plugin').mkdir()
    (root / '.claude-plugin/marketplace.json').write_text('{}\n')
    for name in ['LICENSE', 'THIRD_PARTY_NOTICES.md', 'VERSION']:
        (root / name).write_text('0.1.0\n' if name == 'VERSION' else 'Synthetic MIT fixture.\n')
    subprocess.run(['git', 'init', '--quiet', str(root)], check=True)
    subprocess.run(['git', 'add', '.'], cwd=root, check=True)
    return root


@pytest.fixture
def built(source, tmp_path):
    (source / 'personal-transcript.txt').write_text('untracked fixture; must not be copied')
    (source / 'domains/example/skills/first/private-session.json').write_text('untracked; must not be copied')
    out = tmp_path / 'release'
    release.build(source, out, '0.1.0', COMMIT)
    return out


def refresh_checksums(directory):
    manifest_path = directory / 'manifest.json'
    data = json.loads(manifest_path.read_text())
    for record in data['assets']:
        path = directory / record['file']
        record.update(bytes=path.stat().st_size, sha256=sha256(path))
    manifest_path.write_bytes(release.encoded(data))
    sums = {r['file']: r['sha256'] for r in data['assets']} | {'manifest.json': sha256(manifest_path)}
    (directory / 'SHA256SUMS').write_text(''.join(f'{digest}  {name}\n' for name, digest in sorted(sums.items())))


def test_full_matrix_and_individual_isolation(built):
    result = verify(built)
    assert result['individual_packages'] == 12 and result['release_assets'] == 24
    manifest = json.loads((built / 'manifest.json').read_text())
    for target, prefix in TARGETS.items():
        record = next(r for r in manifest['assets'] if r['kind'] == 'skill' and r['target'] == target and r['artifacts'] == ['example/first'])
        with zipfile.ZipFile(built / record['file']) as archive:
            names = archive.namelist()
            assert f'{prefix}/first/SKILL.md' in names
            assert f'{prefix}/first/assets/.claude-plugin/plugin.json' in names
            assert f'{prefix}/first/references/catalog-support/example/knowledge/shared.md' in names
            assert not any('/second/' in n for n in names)
            assert not any('private-session' in n for n in names)
            assert 'example/second' not in archive.read('ai-foundation-metadata/INDEX.md').decode()
            assert 'AGENTS.md' not in names
            if target == 'gemini':
                assert 'second' not in archive.read('GEMINI.md').decode()
                assert json.loads(archive.read('gemini-extension.json'))['version'] == '0.1.0'


def test_deterministic_across_source_mtimes(source, built, tmp_path):
    import os
    for path in source.rglob('*'):
        if path.is_file() and '.git' not in path.parts:
            os.utime(path, (1700000000, 1700000000))
    second = tmp_path / 'second'
    release.build(source, second, '0.1.0', COMMIT)
    assert {p.name: sha256(p) for p in built.iterdir()} == {p.name: sha256(p) for p in second.iterdir()}


def test_complete_has_all_constituents_and_only_tracked_native(source, built):
    with zipfile.ZipFile(built / 'ai-foundation-v0.1.0-complete.zip') as archive:
        names = archive.namelist()
        assert 'ai-foundation-0.1.0/native/.claude-plugin/marketplace.json' in names
        assert len([n for n in names if '/by-skill/' in n]) == 12
        assert not any('.git/' in n or 'personal-transcript' in n for n in names)


def test_never_overwrites_output(source, built):
    before = sha256(built / 'manifest.json')
    with pytest.raises(ValueError, match='new directory'):
        release.build(source, built, '0.1.0', COMMIT)
    assert sha256(built / 'manifest.json') == before


@pytest.mark.parametrize('version', ['v0.1.0', '../0.1.0', '01.1.0', '0.1', '0.1.0+unsafe'])
def test_version_rejected_before_output(source, tmp_path, version):
    output = tmp_path / 'invalid'
    with pytest.raises(ValueError, match='SemVer'):
        release.build(source, output, version, COMMIT)
    assert not output.exists()


def test_symlink_is_not_followed(source, tmp_path):
    link = source / 'domains/example/skills/first/private'
    link.symlink_to(source / 'LICENSE')
    subprocess.run(['git', 'add', '.'], cwd=source, check=True)
    with pytest.raises(ValueError, match='non-regular tracked'):
        release.build(source, tmp_path / 'bad', '0.1.0', COMMIT)
    assert not (tmp_path / 'bad').exists()


def test_untracked_skill_symlink_is_not_followed(source, tmp_path):
    link = source / 'domains/example/skills/first/private'
    link.symlink_to(source / 'LICENSE')
    with pytest.raises(ValueError, match='symlink'):
        release.build(source, tmp_path / 'bad', '0.1.0', COMMIT)


def test_missing_asset_fails(built):
    next(built.glob('*skill-codex-*.zip')).unlink()
    with pytest.raises(ValueError, match='missing or unexpected'):
        verify(built)


def test_duplicate_zip_member_fails(built):
    path = next(built.glob('*skill-codex-*.zip'))
    with zipfile.ZipFile(path, 'a') as archive:
        with pytest.warns(UserWarning, match='Duplicate name'):
            archive.writestr('LICENSE', 'duplicate')
    refresh_checksums(built)
    with pytest.raises(ValueError, match='duplicate ZIP member'):
        verify(built)


def test_zip_symlink_fails(built):
    import stat
    path = next(built.glob('*skill-codex-*.zip'))
    info = zipfile.ZipInfo('link')
    info.external_attr = (stat.S_IFLNK | 0o777) << 16
    with zipfile.ZipFile(path, 'a') as archive:
        archive.writestr(info, '../outside')
    refresh_checksums(built)
    with pytest.raises(ValueError, match='symlinks'):
        verify(built)


def test_standalone_verifier_needs_no_repository_imports(built, tmp_path):
    import sys
    result = subprocess.run([sys.executable, '-I', str(built / 'verify-release.py'), str(built),
                             '--expected-commit', COMMIT], cwd=tmp_path, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)['individual_packages'] == 12


def test_standalone_verifier_rejects_wrong_source(built, tmp_path):
    import sys
    result = subprocess.run([sys.executable, '-I', str(built / 'verify-release.py'), str(built),
                             '--expected-commit', 'b' * 40], cwd=tmp_path, text=True, capture_output=True)
    assert result.returncode != 0 and 'source commit mismatch' in result.stderr


def test_asset_limit_checked_before_output(source, tmp_path, monkeypatch):
    monkeypatch.setattr(release, 'MAX_ASSETS', 1)
    with pytest.raises(ValueError, match='asset limit'):
        release.build(source, tmp_path / 'bad', '0.1.0', COMMIT)
    assert not (tmp_path / 'bad').exists()


def test_changed_or_missing_asset_fails(built):
    archive = next(built.glob('*skill-codex-*.zip'))
    archive.write_bytes(archive.read_bytes() + b'changed')
    with pytest.raises(ValueError, match='size mismatch|hash mismatch'):
        verify(built)


@pytest.mark.parametrize('member', ['../escape.txt', '/absolute.txt', 'C:/drive.txt', 'safe\\escape.txt'])
def test_traversal_even_with_matching_hash_is_rejected(built, member):
    path = next(built.glob('*skill-codex-*.zip'))
    with zipfile.ZipFile(path, 'a') as archive:
        archive.writestr(member, b'synthetic')
    refresh_checksums(built)
    with pytest.raises(ValueError, match='unsafe package path'):
        verify(built)


def test_skill_identity_tampering_is_rejected(built):
    path = next(built.glob('*skill-codex-*.zip'))
    with zipfile.ZipFile(path, 'a') as archive:
        archive.writestr('.agents/skills/unexpected/SKILL.md', 'not selected')
    refresh_checksums(built)
    with pytest.raises(ValueError, match='identity/count'):
        verify(built)


def test_unexpected_file_and_manifest_checksum_are_rejected(built):
    extra = built / 'unexpected.txt'
    extra.write_text('unexpected')
    with pytest.raises(ValueError, match='unexpected release assets'):
        verify(built)
    extra.unlink()
    (built / 'SHA256SUMS').write_text('bad checksum')
    with pytest.raises(ValueError, match='invalid checksum'):
        verify(built)
