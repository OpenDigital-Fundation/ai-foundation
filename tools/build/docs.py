"""Generate navigable indexes from the catalog. Never edit the outputs by hand.

python -m tools.build docs
  domains/<domain>/README.md   what the plugin contains, how to install it, where each artifact came from
  docs/CATALOG.md              every artifact on one page
  docs/SOURCES.md              every upstream source: licence, policy, what was used where, what was excluded
"""
from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path

import yaml

from tools.build.marketplace import MARKETPLACE
from tools.validate.repo import discover

HEADER = "<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->\n\n"


def _cell(text: str, limit: int = 220) -> str:
    text = " ".join(str(text).split()).replace("|", "\\|")
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def _load(root: Path):
    cat = yaml.safe_load((root / "catalog/catalog.yaml").read_text())["artifacts"]
    exc = yaml.safe_load((root / "catalog/exclusions.yaml").read_text())["excluded"]
    domains = yaml.safe_load((root / "catalog/domains.yaml").read_text())["domains"]
    lock = yaml.safe_load((root / "catalog/sources.lock.yaml").read_text())["sources"]
    inv = list(csv.DictReader((root / "catalog/inventory/artifacts.csv").open()))
    arts = {a.id: a for a in discover(root)}
    prov = defaultdict(set)  # artifact id -> upstream sources (from PROVENANCE.yaml)
    for p in (root / "domains").glob("*/PROVENANCE.yaml"):
        domain = p.parent.name
        for f in yaml.safe_load(p.read_text()).get("files") or []:
            parts = f["path"].split("/")
            aid = f"{domain}/{parts[1]}" if parts[0] in {"skills", "workflows"} else f"{domain}/{parts[-1].split('.')[0]}"
            if parts[0] == "agents":
                aid = f"{domain}/{parts[1].removesuffix('.md')}"
            if parts[0] == "knowledge":
                aid = f"{domain}/{parts[1].split('.')[0]}"
            for d in f["derived_from"]:
                prov[aid].add(d["source"])
    for a in cat:  # supersedes also attribute sources (e.g. folded items)
        for k in a.get("supersedes", []):
            prov[a["id"]].add(k.split(":")[0])
    return cat, exc, domains, lock, inv, arts, prov


def _description(arts, aid: str, fallback: str) -> str:
    a = arts.get(aid)
    if a and a.frontmatter and a.frontmatter.get("description"):
        return str(a.frontmatter["description"])
    return fallback


def domain_readme(root, d, boundary, cat, arts, prov, facets=None, vocab=None) -> str:
    items = sorted((a for a in cat if a["id"].startswith(d + "/")), key=lambda a: (a["type"], a["id"]))
    lines = [f"# `{d}`", "", HEADER.strip(), "", boundary, "",
             "[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · "
             "[Manutenção](../../docs/architecture/repository-layout.md)", "", "## Instalação", "", "```text",
             "/plugin marketplace add OpenDigital-Fundation/ai-foundation", f"/plugin install {d}@{MARKETPLACE}", "```", "",
             "## Conteúdo", "", "As descrições abaixo vêm dos artefatos e mantêm seu idioma original.", ""]
    for kind in sorted({a["type"] for a in items}):
        lines += [f"### {kind}", "", "| Artefato | Estado | Quando usar |", "|---|---|---|"]
        for a in (a for a in items if a["type"] == kind):
            art = arts[a["id"]]
            link = f"[`{art.name}`]({art.path.relative_to(root / 'domains' / d).as_posix()})"
            lines.append(f"| {link} | {a['status']} | {_cell(_description(arts, a['id'], a['capability']))} |")
        lines.append("")
    if not items:
        lines += ["Ainda não há artefatos neste domínio.", ""]
    lines += ["## Origem e manutenção", "",
              f"- Entrada editorial: [manifesto de `{d}`](../../catalog/curation/domains/{d}.yaml).",
              f"- Requisitos: [spec do domínio](../../docs/specs/{d}/catalog/spec.md).",
              "- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).",
              "- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em "
              f"`catalog/overrides/{d}/<skill>/`. Consulte o guia antes de editar.", "",
              "| Artefato | Fontes |", "|---|---|"]
    for a in items:
        lines.append(f"| `{a['id'].split('/')[1]}` | {', '.join(sorted(prov.get(a['id'], []))) or 'contribuição original'} |")
    return "\n".join(lines) + "\n"


def catalog_md(root, cat, domains, arts) -> str:
    by = defaultdict(list)
    for a in cat:
        by[a["id"].split("/")[0]].append(a)
    types = Counter(a["type"] for a in cat)
    lines = ["# Catálogo de artefatos", "", HEADER.strip(), "",
             f"{len(cat)} artefatos em {len(domains)} domínios. Tipos: " + ", ".join(f"{n} {kind}" for kind, n in sorted(types.items())) + ".", "",
             "[Início](../README.md) · [Buscar por faceta](FACETS.md) · [Como manter](architecture/repository-layout.md)", "",
             "## Domínios", ""]
    lines += [f"- [{d}](#{d}) — {len(by[d])} artefatos" for d in sorted(domains)]
    lines.append("")
    for d in sorted(domains):
        lines += [f"## {d}", "", f"[Plugin e instalação](../domains/{d}/README.md) · "
                  f"[Manifesto editorial](../catalog/curation/domains/{d}.yaml)", "", domains[d], "",
                  "| Artefato | Tipo | Capacidade |", "|---|---|---|"]
        for a in sorted(by[d], key=lambda a: a["id"]):
            art = arts[a["id"]]
            target = art.path.relative_to(root).as_posix()
            lines.append(f"| [`{a['id'].replace('/', ':')}`](../{target}) | {a['type']} | {_cell(a['capability'])} |")
        lines.append("")
    return "\n".join(lines)


def sources_md(root, cat, exc, lock, inv, prov) -> str:
    inv_by_src = Counter(r["source"] for r in inv)
    absorbed = defaultdict(set)
    for a in cat:
        for k in a.get("supersedes", []):
            absorbed[k.split(":")[0]].add(a["id"])
    for aid, srcs in prov.items():
        for s in srcs:
            absorbed[s].add(aid)
    excluded = defaultdict(Counter)
    for e in exc:
        excluded[e["key"].split(":")[0]][e["reason"]] += 1
    knowledge = {p.relative_to(root).as_posix(): p.read_text() for p in (root / "domains").rglob("*.md")}
    lines = ["# Sources", "", HEADER.strip(), "",
             "Every upstream source evaluated for this catalog, pinned in `catalog/sources.lock.yaml`. "
             "`merge` sources may be copied and adapted (with provenance); `reference` sources are only linked.", "",
             "| Source | Licence | Policy | Upstream items | Used in artifacts | Excluded |", "|---|---|---|---|---|---|"]
    for s in lock:
        sid = s["id"]
        ex = ", ".join(f"{n} {r}" for r, n in excluded[sid].most_common()) or "—"
        lines.append(f"| [{sid}]({s['url']}) @ `{s['commit'][:7]}` | {s['license']} | {s['policy']} | {inv_by_src.get(sid, 0)} | "
                     f"{len(absorbed.get(sid, ()))} | {ex} |")
    lines.append("")
    for s in lock:
        sid = s["id"]
        lines += [f"## {sid}", "", f"- URL: <{s['url']}> · commit `{s['commit']}` · licence {s['license']} · policy `{s['policy']}`"]
        if s.get("note"):
            lines.append(f"- Note: {s['note']}")
        used = sorted(absorbed.get(sid, ()))
        if used:
            lines += ["- Used in: " + ", ".join(f"`{u.replace('/', ':')}`" for u in used)]
        if s["policy"] == "reference":
            where = sorted(p for p, t in knowledge.items() if s["url"] in t or sid in t)
            lines.append("- Referenced (not copied) from: " + (", ".join(f"[`{w}`](../{w})" for w in where) or "**nowhere — add a reference**"))
        if excluded[sid]:
            lines.append("- Excluded items by reason: " + ", ".join(f"{r}: {n}" for r, n in excluded[sid].most_common()))
        lines.append("")
    contrib = root / "catalog/contributions.yaml"
    if contrib.is_file():
        lines += ["## Original OpenDigital contributions", "", "Skills written by OpenDigital people, generalised and brought into the catalog "
                  "(client-specific details removed).", "", "| Contribution | Authors | Original language | Used in | How |", "|---|---|---|---|---|"]
        for c in yaml.safe_load(contrib.read_text()).get("contributions") or []:
            lines.append(f"| {c['title']} | {', '.join(c['authors'])} | {c['language']} | "
                         + ", ".join(f"`{x.replace('/', ':')}`" for x in c["artifacts"]) + f" | {_cell(c['how'])} |")
        lines.append("")
    lines += ["Licence texts and copyright notices: [`THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md). "
              "Per-file origin: each domain's `PROVENANCE.yaml`. Per-item decisions: `catalog/catalog.yaml` (`supersedes`) and "
              "`catalog/curation/exclusions.yaml`.", ""]
    return "\n".join(lines)


def _vocab(root: Path) -> dict[str, dict[str, dict]]:
    out = {}
    for f in ("technology", "knowledge", "capabilities", "industries", "multidisciplinary"):
        p = root / "catalog/taxonomy" / f"{f}.yaml"
        out[f] = {t["id"]: t for t in yaml.safe_load(p.read_text())["terms"]} if p.is_file() else {}
    return out


def facets_md(root: Path, cat, vocab, facets) -> str:
    labels = {"capabilities": "Capacidade", "knowledge": "Conhecimento", "technology": "Tecnologia",
              "industries": "Setor", "multidisciplinary": "Área multidisciplinar"}
    paths = {a.id: a.path.relative_to(root).as_posix() for a in discover(root)}
    lines = ["# Buscar por faceta", "", HEADER.strip(), "",
             "Um artefato tem um domínio dono e pode aparecer em várias facetas. "
             "As listas abaixo abrem os arquivos canônicos; não são cópias nem novos plugins.", "",
             "[Catálogo por domínio](CATALOG.md) · [Contrato das facetas](adr/foundation/faceted-classification.md) · "
             "[Vocabulários](../catalog/taxonomy/)", "",
             "Termos marcados como propostos aguardam revisão humana.", ""]
    lines += [f"- [{label}](#{facet})" for facet, label in labels.items()]
    lines.append("")
    for facet, label in labels.items():
        index = defaultdict(list)
        for aid, assignment in facets.items():
            for value in assignment.get(facet, []):
                index[value].append(aid)
        lines += [f'<a id="{facet}"></a>', "", f"## {label}", ""]
        for term_id in sorted(index, key=lambda i: (vocab[facet].get(i, {}).get("parent", i), i)):
            term = vocab[facet].get(term_id, {})
            name = term.get("name", {}).get("pt", term_id)
            parent = term.get("parent")
            prefix = f"{vocab[facet][parent]['name']['pt']} › " if parent and parent in vocab[facet] else ""
            mark = " — proposto" if term.get("origin") == "proposed" else ""
            from html import escape
            lines += ["<details>", f"<summary>{escape(prefix + name)} ({len(index[term_id])}){mark}</summary>", ""]
            lines += [f"- [`{aid.replace('/', ':')}`](../{paths[aid]})" for aid in sorted(index[term_id])]
            lines += ["", "</details>", ""]
    return "\n".join(lines)


def write_all(root: Path) -> list[Path]:
    cat, exc, domains, lock, inv, arts, prov = _load(root)
    vocab = _vocab(root)
    facets_p = root / "catalog/facets.yaml"
    facets = (yaml.safe_load(facets_p.read_text()).get("artifacts") or {}) if facets_p.is_file() else {}
    written = []
    for d, boundary in domains.items():
        p = root / "domains" / d / "README.md"
        p.write_text(domain_readme(root, d, boundary, cat, arts, prov, facets, vocab))
        written.append(p)
    outputs = [("CATALOG.md", catalog_md(root, cat, domains, arts)), ("SOURCES.md", sources_md(root, cat, exc, lock, inv, prov))]
    if facets:
        outputs.append(("FACETS.md", facets_md(root, cat, vocab, facets)))
    for name, text in outputs:
        p = root / "docs" / name
        p.write_text(text)
        written.append(p)
    return written
