"""Read the one editorial manifest owned by each domain."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import jsonschema
import yaml

REGISTRY_FIELDS = {"id", "type", "capability", "status", "owner", "supersedes", "path"}


def _validate(root: Path, name: str, data, label: str) -> None:
    schema = json.loads((root / "catalog/schema" / f"{name}.schema.json").read_text())
    errors = sorted(jsonschema.Draft202012Validator(schema).iter_errors(data), key=lambda e: str(e.path))
    if errors:
        raise ValueError(f"{label}: {errors[0].message}")


def load(root: Path, overrides: dict[str, dict] | None = None) -> dict[str, dict]:
    domains = yaml.safe_load((root / "catalog/domains.yaml").read_text())["domains"]
    directory = root / "catalog/curation/domains"
    paths = {p.stem: p for p in directory.glob("*.yaml")}
    if set(paths) != set(domains):
        raise ValueError(f"catalog/curation/domains: missing {sorted(set(domains) - set(paths))}; "
                         f"unknown {sorted(set(paths) - set(domains))}")
    result, seen = {}, set()
    for domain in sorted(paths):
        path = paths[domain]
        data = overrides[domain] if overrides is not None and domain in overrides else yaml.safe_load(path.read_text())
        label = path.relative_to(root).as_posix()
        _validate(root, "curation", data, label)
        if data["domain"] != domain:
            raise ValueError(f"{label}: domain must equal '{domain}'")
        entries = []
        for artifact in data["artifacts"]:
            aid = artifact["id"]
            if aid.split("/")[0] != domain:
                raise ValueError(f"{label}: '{aid}' belongs to another domain")
            if aid in seen:
                raise ValueError(f"{label}: duplicate artifact '{aid}'")
            seen.add(aid)
            if "recipe" in artifact and "language_pack" in artifact:
                raise ValueError(f"{label}: '{aid}' cannot have both recipe and language_pack")
            if "language_pack" in artifact and domain != "languages":
                raise ValueError(f"{label}: language_pack is only valid in languages")
            entries.append({k: v for k, v in artifact.items() if k in REGISTRY_FIELDS})
        for mapping in data.get("imports", []):
            parts = Path(mapping["dest"]).parts
            if len(parts) < 3 or parts[:2] != ("domains", domain) or ".." in parts:
                raise ValueError(f"{label}: import destination must stay inside domains/{domain}")
        _validate(root, "catalog", {"version": 1, "artifacts": entries}, label)
        result[domain] = data
    return result


def projections(root: Path, manifests: dict | None = None, exclusions: dict | None = None) -> tuple[dict, dict]:
    manifests = load(root, manifests)
    artifacts = sorted(({k: v for k, v in a.items() if k in REGISTRY_FIELDS}
                        for m in manifests.values() for a in m["artifacts"]), key=lambda a: a["id"])
    if exclusions is None:
        exclusions = yaml.safe_load((root / "catalog/curation/exclusions.yaml").read_text())
    _validate(root, "exclusions", exclusions, "catalog/curation/exclusions.yaml")
    keys = [key for artifact in artifacts for key in artifact.get("supersedes", [])]
    keys += [entry["key"] for entry in exclusions.get("excluded") or []]
    duplicates = sorted(key for key, count in Counter(keys).items() if count > 1)
    if duplicates:
        raise ValueError(f"catalog/curation: upstream items decided more than once: {duplicates}")
    exclusions["excluded"] = sorted(exclusions.get("excluded") or [], key=lambda e: e["key"].lower())
    return {"version": 1, "artifacts": artifacts}, exclusions


def language_packs(root: Path) -> dict:
    return {"packs": {a["id"].split("/")[1]: a["language_pack"]
                      for m in load(root).values() for a in m["artifacts"] if "language_pack" in a}}
