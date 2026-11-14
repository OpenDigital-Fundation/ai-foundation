"""Verify a downloaded release offline; never extract or execute its contents."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import tomllib
import zipfile

TARGETS = {
    'claude-code': '.claude/skills',
    'codex': '.agents/skills',
    'cursor': '.agents/skills',
    'gemini': 'skills',
    'opencode': '.opencode/skills',
    'github-copilot': '.github/skills',
}
MAX_ASSETS = 1000
MAX_ASSET_BYTES = 2 * 1024 ** 3
MAX_EXPANDED_BYTES = 4 * 1024 ** 3


def sha256(path: Path) -> str:
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def safe_name(name: str) -> None:
    path = PurePosixPath(name)
    if (not name or path.is_absolute() or '..' in path.parts or '\\' in name
            or ':' in name or path.as_posix() != name or name == '.'):
        raise ValueError(f'unsafe package path: {name}')


def inspect_zip(path: Path, record: dict, artifacts: dict, version: str) -> None:
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        names = {i.filename for i in infos}
        if len(infos) != len(names) or len(infos) > 200_000:
            raise ValueError('duplicate ZIP member or excessive member count')
        if sum(i.file_size for i in infos) > MAX_EXPANDED_BYTES:
            raise ValueError('ZIP expanded size limit exceeded')
        for info in infos:
            safe_name(info.filename)
            if info.is_dir() or stat.S_IFMT(info.external_attr >> 16) not in {0, stat.S_IFREG}:
                raise ValueError('ZIP symlinks and non-regular members are forbidden')
        if archive.testzip() is not None:
            raise ValueError('ZIP CRC check failed')
        if record['kind'] == 'complete':
            prefix = f'ai-foundation-{version}/'
            if not all(n.startswith(prefix) for n in names):
                raise ValueError('complete package has an unexpected root')
            required = {prefix + n for n in ['manifest.json', 'INSTALL.md', 'native/LICENSE',
                                            'native/THIRD_PARTY_NOTICES.md', 'native/.claude-plugin/marketplace.json']}
            if not required <= names:
                raise ValueError('complete package missing native metadata')
            native = {n for n in names if re.fullmatch(re.escape(prefix) + r'native/domains/[^/]+/(skills|workflows)/[^/]+/SKILL.md', n)}
            if len(native) != len(artifacts):
                raise ValueError('complete native skill count mismatch')
            return
        selected = record['artifacts']
        target = record['target']
        skill_root = TARGETS.get(target, '')
        public = {f'{skill_root}/{artifacts[a]["name"]}/SKILL.md'.lstrip('/') for a in selected}
        actual = {n for n in names if n.endswith('/SKILL.md') and len(PurePosixPath(n).parts) == len(PurePosixPath(skill_root).parts) + 2}
        if actual != public:
            raise ValueError('public skill identity/count mismatch')
        for a in selected:
            metadata = f'ai-foundation-metadata/{a.replace("/", "--")}/'
            if not {metadata + n for n in ['artifact.json', 'PROVENANCE.yaml']} <= names:
                raise ValueError('missing artifact provenance')
            data = json.loads(archive.read(metadata + 'artifact.json'))
            if data['id'] != a or data['status'] != artifacts[a]['status']:
                raise ValueError('artifact metadata mismatch')
        if not {'LICENSE', 'THIRD_PARTY_NOTICES.md', 'INSTALL.md'} <= names:
            raise ValueError('missing package license or install guide')
        if target == 'cursor':
            rules = {n for n in names if n.startswith('.cursor/rules/') and n.endswith('.mdc')}
            if rules != {f'.cursor/rules/{artifacts[a]["name"]}.mdc' for a in selected}:
                raise ValueError('Cursor rule selection mismatch')
        if target == 'gemini':
            manifest = json.loads(archive.read('gemini-extension.json'))
            if manifest['version'] != version or manifest['contextFileName'] != 'GEMINI.md':
                raise ValueError('Gemini extension metadata mismatch')
            commands = {n for n in names if n.startswith('commands/') and n.endswith('.toml')}
            expected = {f'commands/{artifacts[a]["domain"]}/{artifacts[a]["name"]}.toml' for a in selected}
            if commands != expected:
                raise ValueError('Gemini command selection mismatch')
            for command in commands:
                parsed = tomllib.loads(archive.read(command).decode())
                if not parsed.get('description') or '{{args}}' not in parsed.get('prompt', ''):
                    raise ValueError('invalid Gemini command')


def verify(directory: Path) -> dict:
    manifest_path = directory / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    if manifest.get('schema_version') != 1 or manifest.get('targets') != TARGETS:
        raise ValueError('unsupported release manifest')
    version = manifest.get('version', '')
    if not re.fullmatch(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)', version):
        raise ValueError('invalid release version')
    artifacts = {a['id']: a for a in manifest['artifacts']}
    if not artifacts or len(artifacts) != len(manifest['artifacts']):
        raise ValueError('empty or duplicate artifact set')
    if not re.fullmatch(r'[0-9a-f]{40}', manifest.get('source_commit', '')):
        raise ValueError('invalid source commit')
    records = manifest['assets']
    filenames = [r['file'] for r in records]
    # Two self-describing files cannot include their own digests.
    expected_files = set(filenames) | {'manifest.json', 'SHA256SUMS'}
    if len(filenames) != len(set(filenames)) or len(expected_files) > MAX_ASSETS:
        raise ValueError('duplicate assets or GitHub asset limit exceeded')
    if {p.name for p in directory.iterdir()} != expected_files:
        raise ValueError('missing or unexpected release assets')
    expected_sums = {}
    for record in records:
        filename = record['file']
        safe_name(filename)
        if '/' in filename:
            raise ValueError('release assets must have flat filenames')
        path = directory / filename
        if path.is_symlink() or not path.is_file() or path.stat().st_size != record['bytes']:
            raise ValueError('asset missing or size mismatch')
        if path.stat().st_size >= MAX_ASSET_BYTES:
            raise ValueError('GitHub asset size limit exceeded')
        digest = sha256(path)
        if digest != record['sha256']:
            raise ValueError(f'asset hash mismatch: {filename}')
        expected_sums[filename] = digest
        if record['kind'] in {'skill', 'bundle', 'complete'}:
            inspect_zip(path, record, artifacts, version)
    expected_sums['manifest.json'] = sha256(manifest_path)
    lines = (directory / 'SHA256SUMS').read_text().splitlines()
    actual_sums = {}
    for line in lines:
        if not re.fullmatch(r'[0-9a-f]{64}  [^/\\]+', line):
            raise ValueError('invalid checksum line')
        digest, filename = line.split('  ', 1)
        if filename in actual_sums:
            raise ValueError('duplicate checksum filename')
        actual_sums[filename] = digest
    if actual_sums != expected_sums:
        raise ValueError('checksum manifest mismatch')
    singles = {(r['target'], tuple(r['artifacts'])) for r in records if r['kind'] == 'skill'}
    if singles != {(t, (a,)) for t in TARGETS for a in artifacts} or sum(r['kind'] == 'skill' for r in records) != len(singles):
        raise ValueError('individual package matrix incomplete')
    bundles = [r for r in records if r['kind'] == 'bundle']
    if len(bundles) != len(TARGETS) + 1 or {r['target'] for r in bundles} != set(TARGETS) | {'agent-skills'}:
        raise ValueError('bundle matrix incomplete')
    if any(set(r['artifacts']) != set(artifacts) for r in bundles):
        raise ValueError('bundle artifact set mismatch')
    full = [r for r in records if r['kind'] == 'complete']
    if len(full) != 1:
        raise ValueError('exactly one complete ZIP is required')
    with zipfile.ZipFile(directory / full[0]['file']) as archive:
        embedded = json.loads(archive.read(f'ai-foundation-{version}/manifest.json'))
        if embedded['artifacts'] != manifest['artifacts'] or embedded['source_commit'] != manifest['source_commit']:
            raise ValueError('complete metadata mismatch')
        expected_embedded = [r for r in records if r['kind'] != 'complete']
        if embedded['assets'] != expected_embedded:
            raise ValueError('complete asset matrix mismatch')
        for record in expected_embedded:
            with archive.open(f'ai-foundation-{version}/{record["path"]}') as stream:
                if hashlib.file_digest(stream, 'sha256').hexdigest() != record['sha256']:
                    raise ValueError('complete embedded asset hash mismatch')
    return {'version': version, 'source_commit': manifest['source_commit'], 'artifacts': len(artifacts),
            'targets': len(TARGETS), 'individual_packages': len(singles),
            'release_assets': len(expected_files), 'hashes_verified': True}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--expected-commit')
    args = parser.parse_args()
    try:
        result = verify(args.directory)
        if args.expected_commit and result['source_commit'] != args.expected_commit:
            raise ValueError('release source commit mismatch')
        print(json.dumps(result, sort_keys=True))
    except (ValueError, OSError, KeyError, zipfile.BadZipFile) as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
