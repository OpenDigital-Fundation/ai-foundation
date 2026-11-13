"""Stdlib-only artifact handoff check; never extracts or executes package contents.

python -m tools.build.artifact_smoke pack <adapters> <new-output> --expected-skills <n>
python verify_artifacts.py verify <downloaded-packages>
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import zipfile

ROOTS = {"agent-skills": ("agent-skills",), "cursor": ("cursor", ".agents", "skills"),
         "gemini": ("gemini", "skills"), "opencode": ("opencode", ".opencode", "skills")}
MAX_BYTES = 1024 ** 3


def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def pack(adapters: Path, output: Path, expected_skills: int) -> dict:
    if expected_skills < 1 or output.exists():
        raise ValueError("expected skills must be positive and output must be a new directory")
    if not all((adapters / name).is_dir() for name in ROOTS):
        raise ValueError("all four adapter directories are required")
    output.mkdir(parents=True)
    packages = {}
    for name in ROOTS:
        archive = output / f"ai-foundation-{name}.zip"
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as target:
            for path in sorted((adapters / name).rglob("*")):
                if path.is_symlink():
                    raise ValueError("symlinks are not accepted in smoke packages")
                if path.is_file():
                    target.write(path, path.relative_to(adapters).as_posix())
        packages[name] = {"file": archive.name, "sha256": sha256(archive)}
    shutil.copyfile(Path(__file__), output / "verify_artifacts.py")
    manifest = {"version": 1, "expected_skills": expected_skills, "packages": packages}
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return verify(output)


def verify(directory: Path) -> dict:
    manifest = json.loads((directory / "manifest.json").read_text())
    if manifest.get("version") != 1 or set(manifest.get("packages", {})) != set(ROOTS):
        raise ValueError("manifest must describe exactly four adapter packages")
    expected = manifest.get("expected_skills")
    if type(expected) is not int or expected < 1:
        raise ValueError("expected_skills must be a positive integer")
    counts = {}
    for name, prefix in ROOTS.items():
        record = manifest["packages"][name]
        filename = f"ai-foundation-{name}.zip"
        if record.get("file") != filename:
            raise ValueError("unexpected package filename")
        archive = directory / filename
        if not archive.is_file():
            raise ValueError(f"missing package: {filename}")
        if sha256(archive) != record.get("sha256"):
            raise ValueError(f"package hash mismatch: {filename}")
        with zipfile.ZipFile(archive) as zipped:
            infos = zipped.infolist()
            if len(infos) > 100_000 or sum(i.file_size for i in infos) > MAX_BYTES:
                raise ValueError("package exceeds smoke resource limits")
            names = [i.filename for i in infos]
            if len(names) != len(set(names)):
                raise ValueError("duplicate ZIP entry")
            count = 0
            for info in infos:
                path = PurePosixPath(info.filename)
                if path.is_absolute() or ".." in path.parts or "\\" in info.filename or not path.parts or path.parts[0] != name:
                    raise ValueError("unsafe or unexpected ZIP path")
                if (info.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError("ZIP symlink is not accepted")
                if path.parts[:len(prefix)] == prefix and len(path.parts) == len(prefix) + 2 and path.name == "SKILL.md":
                    count += 1
            if zipped.testzip() is not None:
                raise ValueError("ZIP checksum failure")
            if count != expected:
                raise ValueError(f"skill count mismatch in {name}: {count} != {expected}")
            counts[name] = count
    return {"packages": len(counts), "skills": counts, "hashes_verified": True}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    create = sub.add_parser("pack")
    create.add_argument("adapters", type=Path); create.add_argument("output", type=Path)
    create.add_argument("--expected-skills", type=int, required=True)
    check = sub.add_parser("verify"); check.add_argument("directory", type=Path)
    args = parser.parse_args()
    try:
        result = pack(args.adapters, args.output, args.expected_skills) if args.command == "pack" else verify(args.directory)
    except (ValueError, OSError, zipfile.BadZipFile) as error:
        parser.error(str(error))
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
