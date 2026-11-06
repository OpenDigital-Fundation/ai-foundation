"""Static checks for the catalog. Each check returns a list of error strings."""
from __future__ import annotations

import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path

import jsonschema

from tools.validate.repo import Artifact, discover, load_yaml

MAX_SKILL_LINES = 500
SIMILARITY_FAIL = 0.80
SIMILARITY_WARN = 0.60


def _schema(root: Path, name: str) -> dict:
    return json.loads((root / "catalog/schema" / f"{name}.schema.json").read_text())


def _validate(data, schema, label: str) -> list[str]:
    v = jsonschema.Draft202012Validator(schema)
    return [f"{label}: {'/'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}" for e in v.iter_errors(data)]


# R1 / R2 ------------------------------------------------------------------

def check_registry_files(root: Path) -> list[str]:
    errs: list[str] = []
    for fname, schema in [("catalog.yaml", "catalog"), ("exclusions.yaml", "exclusions"), ("sources.lock.yaml", "sources")]:
        errs += _validate(load_yaml(root / "catalog" / fname), _schema(root, schema), f"catalog/{fname}")
    for prov in sorted((root / "domains").glob("*/PROVENANCE.yaml")):
        errs += _validate(load_yaml(prov), _schema(root, "provenance"), str(prov.relative_to(root)))
    for prof in sorted((root / "profiles").glob("*.yaml")) if (root / "profiles").is_dir() else []:
        errs += _validate(load_yaml(prof), _schema(root, "profile"), str(prof.relative_to(root)))
    return errs


def check_domains(root: Path) -> list[str]:
    declared = set(load_yaml(root / "catalog/domains.yaml")["domains"])
    present = {p.name for p in (root / "domains").iterdir() if p.is_dir()}
    errs = [f"domains/{d}: not declared in catalog/domains.yaml" for d in sorted(present - declared)]
    errs += [f"catalog/domains.yaml: domain '{d}' has no directory" for d in sorted(declared - present)]
    for d in sorted(present & declared):
        pj = root / "domains" / d / ".claude-plugin/plugin.json"
        if not pj.is_file():
            errs.append(f"domains/{d}: missing .claude-plugin/plugin.json")
        else:
            manifest = json.loads(pj.read_text())
            if manifest.get("name") != d:
                errs.append(f"{pj.relative_to(root)}: name must be '{d}'")
            if (root / "domains" / d / "workflows").is_dir() and "./workflows/" not in (manifest.get("skills") or []):
                errs.append(f"{pj.relative_to(root)}: domain has workflows/, so \"skills\" must list \"./skills/\" and \"./workflows/\"")
    return errs


def check_frontmatter(root: Path, arts: list[Artifact]) -> list[str]:
    schema = _schema(root, "frontmatter")
    errs: list[str] = []
    for a in arts:
        if a.type not in {"skill", "workflow", "agent"}:
            continue
        rel = a.path.relative_to(root)
        if a.frontmatter is None:
            errs.append(f"{rel}: missing or invalid YAML frontmatter")
            continue
        errs += _validate(a.frontmatter, schema, str(rel))
        if a.frontmatter.get("name") != a.name:
            errs.append(f"{rel}: frontmatter name '{a.frontmatter.get('name')}' must equal '{a.name}'")
        meta = a.frontmatter.get("metadata") or {}
        if meta.get("domain") not in (None, a.domain):
            errs.append(f"{rel}: metadata.domain '{meta.get('domain')}' must equal '{a.domain}'")
        if a.type in {"skill", "workflow"}:
            lines = a.path.read_text(encoding="utf-8").count("\n")
            exception = str(meta.get("line_budget_exception") or "").strip()
            if lines > MAX_SKILL_LINES and len(exception) < 20:
                errs.append(f"{rel}: {lines} lines exceeds {MAX_SKILL_LINES}; move detail to references/")
        prose = re.sub(r"(?ms)^(```|~~~).*?^\1", "", a.body)
        prose = re.sub(r"`[^`\n]*`", "", prose)
        for link in re.findall(r"\]\((?!https?://|#|mailto:)([^)\s]+)\)", prose):
            target = (a.path.parent / link.split("#")[0]).resolve()
            if not target.exists():
                errs.append(f"{rel}: broken relative link '{link}'")
    return errs


def check_catalog_bijection(root: Path, arts: list[Artifact]) -> list[str]:
    catalog = load_yaml(root / "catalog/catalog.yaml").get("artifacts") or []
    by_id = {e["id"]: e for e in catalog}
    errs = [f"catalog.yaml: duplicate id '{i}'" for i, n in Counter(e["id"] for e in catalog).items() if n > 1]
    found = {a.id: a for a in arts}
    for i, a in found.items():
        if i not in by_id:
            errs.append(f"{a.path.relative_to(root)}: artifact '{i}' is not registered in catalog/catalog.yaml")
        elif by_id[i]["type"] != a.type:
            errs.append(f"catalog.yaml: '{i}' registered as {by_id[i]['type']} but found as {a.type}")
    for i in by_id:
        if i not in found:
            errs.append(f"catalog.yaml: '{i}' has no file under domains/")
    declared = set(load_yaml(root / "catalog/domains.yaml")["domains"])
    for i in by_id:
        if i.split("/")[0] not in declared:
            errs.append(f"catalog.yaml: '{i}' uses undeclared domain")
    # every supersedes/exclusion key is used at most once across the two files
    excluded = load_yaml(root / "catalog/exclusions.yaml").get("excluded") or []
    keys = [k for e in catalog for k in e.get("supersedes", [])] + [e["key"] for e in excluded]
    errs += [f"upstream key '{k}' is decided more than once" for k, n in Counter(keys).items() if n > 1]
    inv = root / "docs/specs/foundation/source-curation/inventory.csv"
    if inv.is_file():
        import csv
        known = {f"{r['source']}:{r['kind']}:{r['name']}" for r in csv.DictReader(inv.open())}
        errs += [f"upstream key '{k}' is not in inventory.csv" for k in keys if k not in known]
    for e in excluded:
        for target in e.get("into", []):
            if target not in by_id:
                errs.append(f"exclusions.yaml: '{e['key']}' points into unknown artifact '{target}'")
    return errs


# R3 -----------------------------------------------------------------------

def check_names(root: Path, arts: list[Artifact]) -> list[str]:
    cfg = load_yaml(root / "catalog/naming.yaml")
    tokens = set(cfg.get("forbidden_tokens", []))
    subs = cfg.get("forbidden_substrings", [])
    errs: list[str] = []
    for name, n in Counter(a.name for a in arts).items():
        if n > 1:
            where = ", ".join(sorted(a.id for a in arts if a.name == name))
            errs.append(f"name '{name}' is used by more than one artifact ({where}); names must be unique repo-wide")
    allowed = set((cfg.get("allowed_names") or {}).keys())
    for a in arts:
        if a.name in allowed:
            continue
        bad = tokens & set(a.name.split("-")) or {s for s in subs if s in a.name}
        if bad:
            errs.append(f"{a.id}: name contains forbidden term(s) {sorted(bad)}")
    return errs


# R4 -----------------------------------------------------------------------

STOP = set("""a an and are as at be by for from in into is it its of on or that the this to use used using when with
you your should any all can not do does what which who will before after while about over under via""".split())


def _tokens(text: str) -> list[str]:
    return [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP and len(w) > 2]


def similarity_matrix(docs: dict[str, str]) -> dict[tuple[str, str], float]:
    toks = {k: Counter(_tokens(v)) for k, v in docs.items()}
    df = Counter(t for c in toks.values() for t in c)
    n = len(docs)
    vec = {}
    for k, c in toks.items():
        v = {t: (1 + math.log(f)) * (math.log((1 + n) / (1 + df[t])) + 1) for t, f in c.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        vec[k] = {t: x / norm for t, x in v.items()}
    keys = sorted(docs)
    out = {}
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            va, vb = vec[a], vec[b]
            if len(va) > len(vb):
                va, vb = vb, va
            out[(a, b)] = sum(x * vb.get(t, 0.0) for t, x in va.items())
    return out


def check_similarity(root: Path, arts: list[Artifact]) -> tuple[list[str], list[str]]:
    allow = {tuple(sorted(p["pair"])) for p in (load_yaml(root / "catalog/similarity-allowlist.yaml").get("pairs") or [])}
    errs, warns = [], []
    for typ in {"skill", "workflow", "agent"}:
        docs = {a.id: str((a.frontmatter or {}).get("description", "")) for a in arts if a.type == typ and a.frontmatter}
        for (a, b), s in similarity_matrix(docs).items():
            if (a, b) in allow:
                continue
            if s >= SIMILARITY_FAIL:
                errs.append(f"{typ}s '{a}' and '{b}' have overlapping triggers (similarity {s:.2f} >= {SIMILARITY_FAIL}); merge them or allowlist with a reason")
            elif s >= SIMILARITY_WARN:
                warns.append(f"{typ}s '{a}' and '{b}' look similar (similarity {s:.2f})")
    return errs, warns


# R5 -----------------------------------------------------------------------

def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_licences(root: Path) -> list[str]:
    errs: list[str] = []
    hashes_file = root / "tools/inventory/reference-hashes.txt"
    if hashes_file.is_file():
        forbidden = {}
        for line in hashes_file.read_text().splitlines():
            if line.strip() and not line.startswith("#"):
                h, src = line.split(None, 1)
                forbidden[h] = src
        for p in (root / "domains").rglob("*"):
            if p.is_file() and p.stat().st_size > 64 and _sha(p) in forbidden:
                errs.append(f"{p.relative_to(root)}: identical to restricted-licence file {forbidden[_sha(p)]}; reference it instead of copying")
    sources = {s["id"]: s for s in load_yaml(root / "catalog/sources.lock.yaml")["sources"]}
    for prov in sorted((root / "domains").glob("*/PROVENANCE.yaml")):
        domain = prov.parent
        for f in load_yaml(prov).get("files") or []:
            if not (domain / f["path"]).exists():
                errs.append(f"{prov.relative_to(root)}: '{f['path']}' does not exist")
            for d in f["derived_from"]:
                s = sources.get(d["source"])
                if not s:
                    errs.append(f"{prov.relative_to(root)}: unknown source '{d['source']}'")
                elif s["policy"] == "reference":
                    errs.append(f"{prov.relative_to(root)}: '{f['path']}' derives from reference-only source '{d['source']}' ({s['license']})")
    return errs


# R6 / R7 ------------------------------------------------------------------

HYGIENE = [
    (re.compile(r"/Users/[A-Za-z0-9._-]+/|/home/[a-z0-9._-]+/|C:\\\\Users\\\\"), "absolute machine path"),
    (re.compile(r"(?i)\b(AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}|sk-[A-Za-z0-9]{32,}|xox[baprs]-[A-Za-z0-9-]{10,})"), "possible secret"),
    (re.compile(r"(?i)-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key"),
    (re.compile(r"(?i)\b(app\.posthog\.com|[a-z]{2}\.i\.posthog\.com|api\.segment\.io|api(-js)?\.mixpanel\.com|api2?\.amplitude\.com|www\.google-analytics\.com|googletagmanager\.com/gtag)\b"), "telemetry endpoint"),
    (re.compile(r"(?i)you (must|MUST) (use|invoke) this skill before any|before ANY response"), "self-promoting activation instruction"),
    (re.compile(r"(?i)\b(auto[- ]?update|self[- ]update)\b.*\b(curl|wget|npm i|npx)\b"), "auto-update instruction"),
]
TEXT_EXT = {".md", ".yaml", ".yml", ".json", ".txt", ".sh", ".py", ".js", ".ts", ".toml"}


def check_hygiene(root: Path) -> list[str]:
    errs: list[str] = []
    for p in sorted((root / "domains").rglob("*")):
        if not p.is_file() or p.suffix not in TEXT_EXT:
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        for rx, label in HYGIENE:
            m = rx.search(text)
            if m:
                line = text.count("\n", 0, m.start()) + 1
                errs.append(f"{p.relative_to(root)}:{line}: {label}")
    for p in sorted((root / "domains").glob("*/mcps/*.json")):
        errs += [f"{p.relative_to(root)}: {e}" for e in _mcp_pin_errors(json.loads(p.read_text()))]
    for p in sorted((root / "domains").glob("*/hooks/hooks.json")):
        if '"enabled": true' in p.read_text():
            errs.append(f"{p.relative_to(root)}: hooks must be opt-in (not enabled by default)")
    return errs


def _mcp_pin_errors(cfg: dict) -> list[str]:
    errs = []
    servers = cfg.get("mcpServers", cfg)
    for name, s in servers.items():
        if not isinstance(s, dict) or "command" not in s:
            continue
        args = [a for a in s.get("args", []) if not a.startswith("-")]
        if s["command"] in {"npx", "bunx", "pnpx", "uvx"} and args:
            pkg = args[0]
            if not re.search(r".@\d", pkg) and not re.search(r"==\d", pkg):
                errs.append(f"server '{name}': package '{pkg}' must be pinned to an exact version")
            if pkg.endswith("@latest"):
                errs.append(f"server '{name}': '@latest' is not allowed")
    return errs


def check_stable_has_evals(root: Path, arts: list[Artifact]) -> list[str]:
    catalog = {e["id"]: e for e in load_yaml(root / "catalog/catalog.yaml").get("artifacts") or []}
    errs = []
    for a in arts:
        if a.type in {"skill", "workflow"} and catalog.get(a.id, {}).get("status") == "stable":
            for f in ("triggers.yaml", "tasks.yaml"):
                if not (a.path.parent / "evals" / f).is_file():
                    errs.append(f"{a.id}: status stable requires evals/{f}")
    return errs


def check_routing_evals(root: Path) -> list[str]:
    ids = {a["id"].replace("/", ":") for a in load_yaml(root / "catalog/catalog.yaml").get("artifacts") or []}
    errs = []
    for f in sorted((root / "evals/routing").glob("*.yaml")) if (root / "evals/routing").is_dir() else []:
        for i, c in enumerate(load_yaml(f) or []):
            exp = c.get("expect")
            if exp not in (None, "none") and exp not in ids:
                errs.append(f"{f.relative_to(root)}[{i}]: expected skill '{exp}' is not in the catalog")
    return errs


def run_all(root: Path) -> tuple[list[str], list[str]]:
    arts = discover(root)
    errs = check_registry_files(root) + check_domains(root)
    errs += check_frontmatter(root, arts) + check_catalog_bijection(root, arts) + check_names(root, arts)
    sim_errs, warns = check_similarity(root, arts)
    errs += sim_errs + check_licences(root) + check_hygiene(root) + check_stable_has_evals(root, arts) + check_routing_evals(root)
    return errs, warns
