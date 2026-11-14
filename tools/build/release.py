"""Build versioned complete, per-client and individual skill ZIPs without installing them."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import stat
import subprocess
import tempfile
import zipfile

from tools.build import adapters
from tools.build.release_verify import MAX_ASSETS, MAX_ASSET_BYTES, TARGETS, safe_name, sha256, verify

Member = Path | bytes


def encoded(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()


def files(base: Path) -> dict[str, Member]:
    result = {}
    for path in sorted(base.rglob('*')):
        if path.is_symlink():
            raise ValueError(f'symlink in distribution source: {path}')
        if path.is_file():
            result[path.relative_to(base).as_posix()] = path
    return result


def write_zip(path: Path, members: dict[str, Member]) -> None:
    with zipfile.ZipFile(path, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for name, value in sorted(members.items()):
            safe_name(name)
            if isinstance(value, Path) and (value.is_symlink() or not value.is_file()):
                raise ValueError(f'not a regular source file: {value}')
            executable = isinstance(value, Path) and bool(value.stat().st_mode & 0o111)
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (stat.S_IFREG | (0o755 if executable else 0o644)) << 16
            archive.writestr(info, value.read_bytes() if isinstance(value, Path) else value, compresslevel=6)
    if path.stat().st_size >= MAX_ASSET_BYTES:
        raise ValueError('GitHub asset size limit exceeded')


def guide(version: str, target: str | None = None) -> bytes:
    text = f'''# OpenDigital AI Foundation {version}

These packages contain experimental capabilities. Structural and integrity checks
do not establish effectiveness or native runtime compatibility of every skill.

## Choose a package

- `complete`: native domain plugins, all client bundles, every individual ZIP and metadata.
- `bundle-<client>`: all skills/workflows for one client.
- `skill-<client>-<domain>--<name>`: exactly one public skill/workflow for that client.
- `bundle-agent-skills`: neutral Agent Skills directories; choose the destination supported by your client.

The archive filenames include their version. `manifest.json` maps canonical IDs,
client, status, source commit and SHA-256. `SHA256SUMS` covers the manifest and every
other asset except itself. `python verify-release.py <download-directory>` verifies
the complete downloaded asset set offline, without extracting or executing it.
The dist complete ZIP contains its constituent assets under by-ai/ and by-skill/;
its embedded manifest deliberately excludes the complete ZIP's own digest.

## Install deliberately

Extract the chosen ZIP into a temporary directory and inspect it first, including
hidden directories. Review existing files before copying anything into a project.
Keep LICENSE, THIRD_PARTY_NOTICES.md and ai-foundation-metadata with the package.
Do not overwrite a project's AGENTS.md, existing rules, skills or settings.

| Client | Package layout / installation |
| --- | --- |
| Claude Code | Copy the selected `.claude/skills/<name>` directories into the project. |
| Codex | Copy the selected `.agents/skills/<name>` directories into the project. |
| GitHub Copilot | Copy the selected `.github/skills/<name>` directories into the project. |
| Cursor | Copy `.agents/skills/<name>` and its `.cursor/rules/<name>.mdc` together. |
| Gemini CLI | Keep the extracted extension directory intact and install that local directory as an extension; its skills/, GEMINI.md, manifest and commands/ belong together. |
| OpenCode | Copy the selected `.opencode/skills/<name>` directories into the project. |
| Agent Skills | Copy selected `<name>` directories into a skills location documented by your client. |

Install only one projection of the same capability in a client to avoid duplicate
discovery. Individual packages have selection-specific indices in
ai-foundation-metadata; they do not announce other skills as installed. The
skill-discovery asset searches the entire catalog and does not imply installation.

The native/ tree in the complete ZIP preserves domain plugins and their marketplace.
The distribution version is separate from plugin versions recorded in that tree.

## Runtime limits

Provider-specific tools mentioned by a skill still require the corresponding host.
Session Lens is an optional private asset for Claude Code; it is not activated by
extracting these packages and is not a Codex, Copilot, Cursor or Orca usage adapter.
No global installation, hooks, telemetry, credential access, personal transcript
collection or model evaluation is performed by the build or verifier.
'''
    if target:
        text += f'\nSelected package: {target}.\n'
    return text.encode()


def metadata(root: Path, entries: list[dict], version: str, commit: str, portable: Path) -> dict[str, Member]:
    result: dict[str, Member] = {
        'LICENSE': root / 'LICENSE',
        'THIRD_PARTY_NOTICES.md': root / 'THIRD_PARTY_NOTICES.md',
        'INSTALL.md': guide(version),
    }
    index = ['# Included capabilities', '', 'Read the installed SKILL.md when its description matches the task.', '']
    support_domains = set()
    for entry in entries:
        base = f'ai-foundation-metadata/{entry["id"].replace("/", "--")}/'
        result[base + 'artifact.json'] = encoded({k: entry[k] for k in ['id', 'name', 'domain', 'status']} | {
            'version': version, 'source_commit': commit, 'type': entry['type'],
            'canonical_path': entry['dir'].relative_to(root).as_posix(),
            'validation': 'experimental; packaging verified, native runtime and task benefit not established',
        })
        result[base + 'PROVENANCE.yaml'] = root / 'domains' / entry['domain'] / 'PROVENANCE.yaml'
        origins = portable / entry['name'] / 'references/catalog-support/origins.json'
        if origins.exists():
            support_domains.update(p.split('/')[1] for p in json.loads(origins.read_text()).values())
        index.append(f'- `{entry["id"]}`: {entry["description"]}')
    for domain in sorted(support_domains):
        result[f'ai-foundation-metadata/support/{domain}/PROVENANCE.yaml'] = root / 'domains' / domain / 'PROVENANCE.yaml'
    result['ai-foundation-metadata/INDEX.md'] = ('\n'.join(index) + '\n').encode()
    return result


def projection(root: Path, staged: Path, entries: list[dict], target: str, version: str, commit: str) -> dict[str, Member]:
    portable = staged / 'agent-skills'
    result = metadata(root, entries, version, commit, portable)
    prefix = TARGETS.get(target, '')
    for entry in entries:
        for name, source in files(portable / entry['name']).items():
            result['/'.join(p for p in [prefix, entry['name'], name] if p)] = source
        if target == 'cursor':
            name = f'.cursor/rules/{entry["name"]}.mdc'
            result[name] = staged / 'cursor' / name
        elif target == 'gemini':
            name = f'commands/{entry["domain"]}/{entry["name"]}.toml'
            result[name] = staged / 'gemini' / name
    if target == 'gemini':
        suffix = '' if len(entries) != 1 else '-' + entries[0]['name']
        result['gemini-extension.json'] = encoded({'name': 'opendigital-ai-foundation' + suffix,
                                                   'version': version, 'contextFileName': 'GEMINI.md'})
        result['GEMINI.md'] = ('# OpenDigital AI Foundation\n\n' + '\n'.join(
            f'- Read `skills/{e["name"]}/SKILL.md` when this task matches: {e["description"]}' for e in entries) + '\n').encode()
    return result


def native(root: Path) -> dict[str, Member]:
    result = {}
    # Git's tracked set is the allow-list: no untracked caches, personal settings,
    # build evidence or source clones enter the complete distribution.
    tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).split(b'\0')
    forbidden = {'.git', '.agents', '.codex', '.aws', '.claude', '.venv', '__pycache__', 'node_modules', '.pytest_cache', '.DS_Store', 'dist'}
    for raw in tracked:
        if not raw:
            continue
        name = raw.decode()
        safe_name(name)
        if any(part in forbidden for part in Path(name).parts):
            raise ValueError(f'non-source file tracked in distribution: {name}')
        path = root / name
        if path.is_symlink() or not path.is_file():
            raise ValueError(f'non-regular tracked source: {name}')
        result['native/' + name] = path
    return result


def build(root: Path, output: Path, version: str, commit: str) -> dict:
    root, output = root.resolve(), output.resolve()
    if not re.fullmatch(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)', version):
        raise ValueError('version must be numeric SemVer without a v prefix')
    if not re.fullmatch(r'[0-9a-f]{40}', commit):
        raise ValueError('source commit must be a complete Git SHA')
    if output.exists():
        raise ValueError('release output must be a new directory; existing files are never removed')
    entries = adapters._entries(root)
    kinds = {a.id: a.type for a in adapters.discover(root)}
    for entry in entries:
        entry['type'] = kinds[entry['id']]
    if not entries or len({e['name'] for e in entries}) != len(entries):
        raise ValueError('release requires non-empty, uniquely named skills')
    # 6 individual matrices, 7 bundles, complete ZIP, guide, verifier, manifest and sums.
    count = len(entries) * len(TARGETS) + len(TARGETS) + 6
    if count > MAX_ASSETS:
        raise ValueError(f'GitHub asset limit exceeded: {count} > {MAX_ASSETS}')
    native_members = native(root)  # Preflight untrusted paths before copying anything.
    for entry in entries:
        for source in entry['dir'].rglob('*'):
            if source.is_symlink():
                raise ValueError(f'symlink in skill source: {source}')
    manifest = {'schema_version': 1, 'version': version, 'source_commit': commit,
                'targets': TARGETS, 'artifacts': [{k: e[k] for k in ['id', 'domain', 'name', 'status', 'type']} for e in entries],
                'assets': []}
    output.mkdir(parents=True)

    def add_file(path: Path, kind: str, relative: str, target=None, selected=None):
        record = {'file': path.name, 'path': relative, 'kind': kind, 'bytes': path.stat().st_size, 'sha256': sha256(path)}
        if target:
            record.update(target=target, artifacts=[e['id'] for e in selected])
        manifest['assets'].append(record)

    with tempfile.TemporaryDirectory(prefix='ai-foundation-release-') as temporary:
        stage = Path(temporary) / 'adapters'
        snapshot = Path(temporary) / 'source'
        for name, source in native_members.items():
            destination = snapshot / name.removeprefix('native/')
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        # Development adapters can copy untracked files from their source tree;
        # release adapters only see the allow-listed tracked snapshot.
        adapters.build_all(snapshot, stage)
        for target in [*TARGETS, 'agent-skills']:
            archive = output / f'ai-foundation-v{version}-bundle-{target}.zip'
            write_zip(archive, projection(root, stage, entries, target, version, commit))
            add_file(archive, 'bundle', 'by-ai/' + archive.name, target, entries)
            if target == 'agent-skills':
                continue
            for entry in entries:
                archive = output / f'ai-foundation-v{version}-skill-{target}-{entry["domain"]}--{entry["name"]}.zip'
                write_zip(archive, projection(root, stage, [entry], target, version, commit))
                relative = f'by-skill/{entry["domain"]}/{entry["name"]}/{archive.name}'
                add_file(archive, 'skill', relative, target, [entry])
    install = output / 'INSTALL.md'
    install.write_bytes(guide(version))
    add_file(install, 'guide', install.name)
    verifier = output / 'verify-release.py'
    verifier.write_bytes(Path(__file__).with_name('release_verify.py').read_bytes())
    add_file(verifier, 'verifier', verifier.name)
    complete_members = native_members | {'INSTALL.md': guide(version), 'manifest.json': encoded(manifest)}
    complete_members.update({r['path']: output / r['file'] for r in manifest['assets']})
    archive = output / f'ai-foundation-v{version}-complete.zip'
    write_zip(archive, {f'ai-foundation-{version}/{name}': source for name, source in complete_members.items()})
    add_file(archive, 'complete', archive.name)
    (output / 'manifest.json').write_bytes(encoded(manifest))
    sums = {r['file']: r['sha256'] for r in manifest['assets']} | {'manifest.json': sha256(output / 'manifest.json')}
    (output / 'SHA256SUMS').write_text(''.join(f'{digest}  {name}\n' for name, digest in sorted(sums.items())))
    return verify(output)


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument('--version')
    args = parser.parse_args(argv)
    root = Path.cwd()
    version = (root / 'VERSION').read_text().strip()
    if args.version and args.version != version:
        parser.error('--version must equal VERSION')
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    if subprocess.check_output(['git', 'status', '--porcelain'], text=True).strip():
        parser.error('release source must be committed and clean')
    try:
        print(json.dumps(build(root, args.output, version, commit), sort_keys=True))
    except (ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
