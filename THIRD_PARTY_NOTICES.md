# Third-party notices

Parts of this repository are derived from the projects below. Each derived file is listed, with the
exact upstream path, commit and kind of modification, in the `PROVENANCE.yaml` of its domain
(`domains/<domain>/PROVENANCE.yaml`). Pinned commits are in `catalog/sources.lock.yaml`.

## MIT-licensed sources

The following projects are distributed under the MIT License. Their copyright notices are reproduced
here as the licence requires; the full MIT text is identical to this repository's `LICENSE` with the
copyright line replaced.

| Project | Copyright |
|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) | Copyright (c) 2025 Jesse Vincent |
| [mattpocock/skills](https://github.com/mattpocock/skills) | Copyright (c) 2026 Matt Pocock |
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | Copyright (c) 2026 Affaan Mustafa |
| [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) | Copyright (c) 2025 AgentLand Contributors |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Copyright (c) 2024 Next Level Builder |
| [Nutlope/hallmark](https://github.com/Nutlope/hallmark) | Copyright (c) 2026 Hallmark contributors |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | Copyright (c) 2026 DietrichGebert |
| [SecurityStandards/skill-security-audit](https://github.com/SecurityStandards/skill-security-audit) | Copyright (c) 2025-2026 Cloudflare, Inc. |
| [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | MIT, as declared in the project README (no LICENSE file upstream) |
| [currents-dev/playwright-best-practices-skill](https://github.com/currents-dev/playwright-best-practices-skill) | Copyright © 2026 Currents Software Inc. |
| [Community-Access/accessibility-agents](https://github.com/Community-Access/accessibility-agents) | Copyright (c) 2026 Taylor Arndt |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | MIT as declared per skill (react-best-practices, composition-patterns, react-view-transitions, react-native-skills); skills without a declared licence are not copied |

## Apache-2.0-licensed sources

[anthropics/skills](https://github.com/anthropics/skills) — skills other than `docx`, `pdf`, `pptx`
and `xlsx` are licensed under the Apache License, Version 2.0
(<https://www.apache.org/licenses/LICENSE-2.0>). Files derived from them carry a notice stating that
they were modified, and `PROVENANCE.yaml` records the modification.

## Modified MIT (restricted)

[millionco/react-doctor](https://github.com/millionco/react-doctor) — Copyright (c) 2026 Million Software, Inc. MIT with one modification: using the software or derivatives as AI training, fine-tuning or evaluation data, or reselling it as a hosted service, requires prior written permission. Vendored only in `domains/languages/skills/react-diagnostics/` with its licence text, and excluded from this catalog's evals (`metadata.eval_excluded`) until permission is granted.

## Referenced only (not copied)

These are linked from `knowledge/` files and never copied, because their licence does not permit
redistribution in an MIT, commercially usable repository:

- `anthropics/skills` — `docx`, `pdf`, `pptx`, `xlsx` (proprietary, © Anthropic, PBC)
- `SecurityStandards/agent-pentester` (AGPL-3.0)
- `SecurityStandards/CTOSecurityChecklist`, `SecurityStandards/DevOpsSecurityChecklist` (CC BY-NC-SA 4.0)
- `SecurityStandards/security-standards` (no licence declared)
- `SecurityStandards/agent-reverse-engineer` (MIT; a product/MCP server, referenced rather than vendored)
