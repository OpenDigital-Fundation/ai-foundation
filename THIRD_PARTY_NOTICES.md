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

| [github/awesome-copilot](https://github.com/github/awesome-copilot) | Copyright GitHub, Inc. |
| [wshobson/agents](https://github.com/wshobson/agents) | Copyright (c) 2024 Seth Hobson |
| [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | Copyright (c) 2025 VoltAgent |
| [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates) | Copyright (c) 2025 Daniel (San) Ávila |
| [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills) | Copyright (c) 2025 (the upstream notice names no holder) |
| [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) | Copyright (c) 2025 K-Dense Inc. |
| `davila7/claude-code-templates` — `cli-tool/components/skills/productivity/avoid-ai-writing/LICENSE.txt` | Copyright (c) 2026 Conor Bronsdon |
| `github/awesome-copilot` — `skills/agent-architecture/LICENSE.txt` | Copyright (c) 2026 Stanislav Bankovskii |
| `K-Dense-AI/claude-scientific-skills` — `skills/pacsomatic/LICENSE` | Copyright (c) 2026 Beifang Niu |

## Apache-2.0-licensed sources

[anthropics/skills](https://github.com/anthropics/skills) — skills other than `docx`, `pdf`, `pptx`
and `xlsx` are licensed under the Apache License, Version 2.0
(<https://www.apache.org/licenses/LICENSE-2.0>). Files derived from them carry a notice stating that
they were modified, and `PROVENANCE.yaml` records the modification.

[openai/skills](https://github.com/openai/skills) — skills with an Apache-2.0 `LICENSE.txt` (the `figma-*` skills carry Figma terms and are not copied). Same notice and provenance rules.

[getsentry/skills](https://github.com/getsentry/skills) — Apache-2.0, except `security-review` (CC BY-SA 4.0, linked only). Same notice and provenance rules.

[nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) — the `ui-styling` folder carries its own Apache-2.0 `LICENSE.txt` (the rest of the collection is MIT); `ui/component-styling` is derived from it. Bundled fonts keep their own OFL licence files.

The generator resolves the licence nearest to each copied file, refuses ShareAlike, non-commercial, unlicensed or unaccepted restricted material, and adds the modification notice wherever the effective licence is Apache-2.0.

## Modified MIT (restricted)

[millionco/react-doctor](https://github.com/millionco/react-doctor) — Copyright (c) 2026 Million Software, Inc. MIT with one modification: using the software or derivatives as AI training, fine-tuning or evaluation data, or reselling it as a hosted service, requires prior written permission. Vendored only in `domains/languages/skills/react-diagnostics/` with its licence text, and excluded from this catalog's evals (`metadata.eval_excluded`) until permission is granted.

## Referenced only (not copied)

These are linked from `knowledge/` files and never copied, because their licence does not permit
redistribution in an MIT, commercially usable repository:

- `anthropics/skills` — `docx`, `pdf`, `pptx`, `xlsx` (proprietary, © Anthropic, PBC)
- `SecurityStandards/agent-pentester` (AGPL-3.0)
- `SecurityStandards/CTOSecurityChecklist`, `SecurityStandards/DevOpsSecurityChecklist` (CC BY-NC-SA 4.0)
- `SecurityStandards/security-standards` (no licence declared)
- `trailofbits/skills` and `getsentry/skills` `security-review` (CC BY-SA 4.0)
- `openai/skills` `figma-*` (Figma terms)
- `SecurityStandards/agent-reverse-engineer` (MIT; a product/MCP server, referenced rather than vendored)

The Elsevier elsarticle examples and bibliography styles supplied in the K-Dense venue-templates source declare LPPL. Those six files are not included in this distribution; the venue guide links to the official package instead.
