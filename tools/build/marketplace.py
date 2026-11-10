"""Generate .claude-plugin/marketplace.json: one plugin per domain."""
from __future__ import annotations

import json
from pathlib import Path

import yaml

MARKETPLACE = "opendigital-ai-foundation"


def build_marketplace(root: Path) -> dict:
    domains = yaml.safe_load((root / "catalog/domains.yaml").read_text())["domains"]
    plugins = []
    for name in domains:
        pj = json.loads((root / "domains" / name / ".claude-plugin/plugin.json").read_text())
        plugins.append({"name": name, "source": f"./domains/{name}", "description": pj["description"],
                        "version": pj["version"], "license": pj.get("license", "MIT")})
    return {
        "name": MARKETPLACE,
        "owner": {"name": "OpenDigital"},
        "metadata": {"description": "Curated, deduplicated skills, agents, workflows and rules for AI agents, one plugin per domain."},
        "plugins": plugins,
    }


def write(root: Path) -> Path:
    out = root / ".claude-plugin/marketplace.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(build_marketplace(root), indent=2) + "\n")
    return out
