"""Discovery of catalog artifacts in the repository tree."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)

# type -> (subdirectory, glob, how to derive the name)
LAYOUT = {
    "skill": ("skills", "*/SKILL.md", "parent"),
    "workflow": ("workflows", "*/SKILL.md", "parent"),
    "agent": ("agents", "*.md", "stem"),
    "prompt": ("prompts", "*.md", "stem"),
    "rule": ("rules", "*.md", "stem"),
    "template": ("templates", "*", "stem"),
    "knowledge": ("knowledge", "*", "stem"),
    "mcp": ("mcps", "*.json", "stem"),
    "hook": ("hooks", "*", "stem"),
}
FRONTMATTER_TYPES = {"skill", "workflow", "agent"}


@dataclass
class Artifact:
    domain: str
    type: str
    name: str
    path: Path
    frontmatter: dict | None = None
    body: str = ""
    errors: list[str] = field(default_factory=list)

    @property
    def id(self) -> str:
        return f"{self.domain}/{self.name}"


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def parse_frontmatter(text: str) -> tuple[dict | None, str]:
    m = FRONTMATTER.match(text)
    if not m:
        return None, text
    try:
        data = yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return None, text
    return (data if isinstance(data, dict) else None), text[m.end():]


def discover(root: Path) -> list[Artifact]:
    found: list[Artifact] = []
    domains_dir = root / "domains"
    if not domains_dir.is_dir():
        return found
    for ddir in sorted(p for p in domains_dir.iterdir() if p.is_dir()):
        for typ, (sub, pattern, naming) in LAYOUT.items():
            base = ddir / sub
            if not base.is_dir():
                continue
            for path in sorted(base.glob(pattern)):
                if path.name.startswith(".") or path.name in {"hooks.json", "README.md"} and typ in {"hook", "template", "knowledge"}:
                    continue
                if typ in {"template", "knowledge", "hook"} and path.is_dir():
                    name = path.name
                else:
                    name = path.parent.name if naming == "parent" else path.name.split(".")[0]
                art = Artifact(ddir.name, typ, name, path)
                if typ in FRONTMATTER_TYPES:
                    fm, body = parse_frontmatter(path.read_text(encoding="utf-8"))
                    art.frontmatter, art.body = fm, body
                found.append(art)
    return found
