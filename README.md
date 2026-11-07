# OpenDigital AI Foundation

A curated collection of skills, agents, workflows, prompts, rules, hooks, MCP configs, templates and evals for AI coding agents — **one capability, one artifact**, organised by domain. Built by deduplicating and merging upstream collections (21 repositories evaluated ; 1,118 artifacts reviewed, every one with a recorded decision).

## Install (Claude Code)

```
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install workflow@opendigital-ai-foundation
```

Each domain is a separate plugin, so you install only what you use. Profiles group domains for common roles:

| Profile | Domains |
|---|---|
| `fullstack-web` | principles, workflow, testing, debugging, code-quality, architecture, languages/typescript, ui, ux, accessibility |
| `backend-service` | principles, workflow, testing, debugging, code-quality, architecture, data, platform, security |
| `security-review` | principles, security, code-quality, languages |
| `agent-builder` | principles, workflow, agent-engineering, ai-engineering, testing |
| `product-team` | workflow, product, research, ux, marketing, documents |
| `design-team` | ui, ux, accessibility, brand, creative-media |

`python -m tools.build profile <name>` prints the install commands for a profile.

## Domains

principles · workflow · architecture · code-quality · testing · debugging · security · languages · data · ui · ux · accessibility · brand · creative-media · ai-engineering · agent-engineering · platform · documents · research · product · marketing · sales · finance · legal-compliance · operations

Browse the full catalog in [`docs/CATALOG.md`](docs/CATALOG.md), each domain's contents in `domains/<domain>/README.md`, and every upstream source — licence, what was used where, what was excluded and why — in [`docs/SOURCES.md`](docs/SOURCES.md).

## How it is built

- **Specs and decisions:** [`docs/specs/ROADMAP.md`](docs/specs/ROADMAP.md), one spec, plan and task list per domain, and ADRs in [`docs/adr/`](docs/adr/).
- **Sources:** pinned in [`catalog/sources.lock.yaml`](catalog/sources.lock.yaml); only permissive licences are copied, and every derived file is listed in its domain's `PROVENANCE.yaml` and in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).
- **Generated content:** most skills are assembled by `tools/curation` from decision files in `catalog/decisions/`; local fixes live in `catalog/overrides/`.
- **Quality gates:** `python -m tools.validate` (format, registry, unique unbranded names, duplicate detection, licences, hygiene, links, full inventory coverage) and `python -m tools.evals.triggers --routing` (model-backed routing evals; billed).

## Status

All artifacts are `experimental` until their trigger and task evals pass. See [`AGENTS.md`](AGENTS.md) for contribution rules.
