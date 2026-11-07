"""Build selected domain recipes from already-fetched pinned source files.

python -m tools.curation <sources-dir> --domain <domain>
python -m tools.curation <sources-dir> --all

This rebuilds generated skill directories; review local changes first. Sources are read as
data, never executed. Directly authored skills are not overwritten by this command.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from tools.catalog import rebuild
from tools.curation.manifests import load


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", type=Path)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--domain", action="append", help="Domain to rebuild; may be repeated")
    target.add_argument("--all", action="store_true", help="Rebuild all domain recipes")
    args = parser.parse_args(argv)
    root = Path.cwd()
    manifests = load(root)
    selected = set(manifests) if args.all else set(args.domain)
    unknown = selected - set(manifests)
    if unknown:
        parser.error(f"unknown domains: {sorted(unknown)}")
    if not args.sources.is_dir():
        parser.error("sources directory does not exist; fetch the pinned sources first")
    from tools.curation.inputs import preflight
    recipes = {a["id"]: a["recipe"] for d in selected for a in manifests[d]["artifacts"] if "recipe" in a}
    packs = {a["id"].split("/")[1]: a["language_pack"] for d in selected for a in manifests[d]["artifacts"] if "language_pack" in a}
    preflight(root, args.sources, recipes, packs)
    rebuild(root)
    from tools.curation import bundle, language_pack
    for domain in sorted(selected):
        artifacts = manifests[domain]["artifacts"]
        recipes = {a["id"]: a["recipe"] for a in artifacts if "recipe" in a}
        if recipes:
            bundle.build(root, args.sources, {"artifacts": recipes})
        packs = {a["id"].split("/")[1]: a["language_pack"] for a in artifacts if "language_pack" in a}
        if packs:
            language_pack.build(root, args.sources, {"packs": packs})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
