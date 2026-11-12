---
name: skill-discovery
description: Use when finding and comparing installable agent skills for a specified task, checking the local catalog first and reviewing candidate content, license, compatibility and installation scope.
license: MIT
---

# Skill discovery

## Resolve the capability

Identify the task, domain, harness/version and whether the user wants a recommendation, repository incorporation or an installation. Start with the local catalog and owner skill when available. A request for help doing a task is not automatically a request to install an extension.

## Internal find first

For an internal lookup, use short keywords or a canonical ID with the repository command:

```sh
python -m tools.catalog find "design instrucional" --domain education --type skill --json
python -m tools.catalog find "Session Lens" --json
```

When using an installed/exported skill outside this checkout, run `scripts/find.py` from this skill's resolved directory with Python 3 and the same query/filter flags. It uses the bundled `assets/catalog-index.json`; it needs no package manager, provider API, network or personal configuration. `assets/search-terms.json` supplies curated pt/en aliases. The repository command reads current metadata in memory; the portable snapshot has the catalog's build digest and may lag a newer catalog.

Search returns canonical IDs, type, status, a path in the source repository, lexical match evidence and the universe queried. Presence in the index does not mean the capability is installed in the current client. Ranking is lexical, not a quality score; no match returns an empty list. Inspect the selected owner's actual entry/resources before relying on it. An explicitly internal search does not authorize an external fallback.

## Search and evaluate

1. Translate the task into specific domain/action terms. Consult the local catalog, source repositories and relevant registries; try a narrower query or alternative terms when needed. A leaderboard is a discovery signal, not evidence of quality.
2. Open the actual candidate SKILL.md and relevant resources. Fix a commit/release and inspect the nearest license and declared origins. Check required scripts, network calls, credentials, dependencies, supported host APIs and side effects before recommending it.
3. Compare capability coverage and boundaries with the existing owner. Improve that owner when the intent already exists; propose a new capability only with its domain spec and a distinct trigger.
4. Present a short source-backed comparison: task fit, exact source/version, license, resources reviewed, compatibility, known limits and how to verify the useful behaviour. Popularity and official branding cannot replace this inspection.
5. Separate the selection from mutation. Before an authorized installation, prepare exact package/ref, target path/scope, effects and recovery. Follow the host's approval policy; do not run a floating npx command, global install, auto-confirm flag or mass update as part of discovery.

If no candidate covers the task, say which search/scope was checked and either do the task directly or propose an addition through agent-engineering:skill-authoring. Do not invent a package or install counts. [Discovery playbook](references/discovery-playbook.md) adapts the reviewed upstream.
