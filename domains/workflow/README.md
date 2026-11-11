# `workflow`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

Delivery lifecycle - ideation, specs, plans, execution, worktrees, branch completion, handoff, retrospectives, tickets.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install workflow@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### knowledge

| Artefato | Estado | Quando usar |
|---|---|---|
| [`issue-tracking`](knowledge/issue-tracking) | experimental | How to create, link, label and query issues on GitHub, GitLab or local markdown trackers. |

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`brainstorming`](skills/brainstorming/SKILL.md) | experimental | Use before building anything non-trivial that is not fully specified yet (a feature, component, behaviour change, new project, or a non-software plan) to find out what the user actually wants and why, compare approaches… |
| [`executing-plans`](skills/executing-plans/SKILL.md) | experimental | Use when an approved implementation plan (plan.md and tasks.md) exists and it is time to build it. Runs the tasks to completion either by dispatching a fresh implementer and reviewer subagent per task, or inline in the… |
| [`finishing-a-branch`](skills/finishing-a-branch/SKILL.md) | experimental | Use when implementation is complete, all tests pass, and you need to decide how to integrate the work |
| [`git-worktrees`](skills/git-worktrees/SKILL.md) | experimental | Use when starting feature work that needs isolation from current workspace or before executing implementation plans - ensures an isolated workspace exists via native tools or git worktree fallback |
| [`grilling`](skills/grilling/SKILL.md) | experimental | Use when the user wants an existing plan, design, decision or idea stress-tested, or says 'grill me'. Interviews them in rounds over a design tree: asks every question whose prerequisites are settled, gives a recommende… |
| [`handoff`](skills/handoff/SKILL.md) | experimental | Use when work must pause and be resumed by another session, another agent or another person - the user says "handoff", "pass the baton", "document where we stopped", "I'll pause here", the context window is nearly full,… |
| [`initiative-mapping`](skills/initiative-mapping/SKILL.md) | experimental | Use when the user brings an idea too big and too foggy for one agent session and wants the way forward charted before anyone builds. Creates a map issue of decision tickets (research, prototype, grilling) on the tracker… |
| [`issue-breakdown`](skills/issue-breakdown/SKILL.md) | experimental | Use when the user asks to turn an approved spec, plan or conversation into issues or tickets. Breaks the work into tracer-bullet vertical slices (or expand-migrate-contract batches for wide refactors), each with its blo… |
| [`issue-triage`](skills/issue-triage/SKILL.md) | experimental | Use when the user asks to triage issues or external pull requests. Moves each through triage roles (needs-triage, needs-info, ready-for-agent, ready-for-human, wontfix), verifies reports against the code, grills where n… |
| [`writing-plans`](skills/writing-plans/SKILL.md) | experimental | Use when an approved spec or clear requirements exist for multi-step work and code has not been touched yet. Writes plan.md (architecture, global constraints, file map, review focus) and tasks.md (bite-sized TDD tasks w… |

### workflow

| Artefato | Estado | Quando usar |
|---|---|---|
| [`feature-delivery`](workflows/feature-delivery/SKILL.md) | experimental | Use when the user wants a feature, behaviour change or new project taken all the way from idea to a merge-ready branch. Orchestrates the delivery skills in order (design, spec, plan, isolated execution with TDD, verific… |

## Origem e manutenção

- Entrada editorial: [manifesto de `workflow`](../../catalog/curation/domains/workflow.yaml).
- Requisitos: [spec do domínio](../../docs/specs/workflow/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/workflow/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `issue-tracking` | mattpocock/skills |
| `brainstorming` | affaan-m/ECC, mattpocock/skills, msitarzewski/agency-agents, obra/superpowers |
| `executing-plans` | affaan-m/ECC, github/awesome-copilot, mattpocock/skills, obra/superpowers |
| `finishing-a-branch` | affaan-m/ECC, mattpocock/skills, obra/superpowers |
| `git-worktrees` | obra/superpowers |
| `grilling` | davila7/claude-code-templates, mattpocock/skills |
| `handoff` | affaan-m/ECC, mattpocock/skills |
| `initiative-mapping` | mattpocock/skills, msitarzewski/agency-agents |
| `issue-breakdown` | affaan-m/ECC, github/awesome-copilot, mattpocock/skills |
| `issue-triage` | Community-Access/accessibility-agents, affaan-m/ECC, mattpocock/skills |
| `writing-plans` | Jeffallan/claude-skills, affaan-m/ECC, davila7/claude-code-templates, github/awesome-copilot, obra/superpowers |
| `feature-delivery` | affaan-m/ECC |
