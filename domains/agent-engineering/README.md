# `agent-engineering`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

Configuring and operating coding agents - skill authoring, harnesses, orchestration, subagents, loops, memory, context.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install agent-engineering@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`agent-debugging`](skills/agent-debugging/SKILL.md) | experimental | Use when an agent run failed, looped, ignored instructions or produced a bad result and you need to know why: capture the transcript, diagnose the failure, contain and recover, and write an introspection report with fix… |
| [`agent-evaluation`](skills/agent-evaluation/SKILL.md) | experimental | Use when measuring agents rather than a single skill: comparing coding agents or configurations head to head on custom tasks, building an eval harness with pass rate, cost and time, self-evaluation of finished work, and… |
| [`agent-guardrails`](skills/agent-guardrails/SKILL.md) | experimental | Use when an agent should be prevented from destructive or risky actions: blocking dangerous git and shell commands (push, reset --hard, clean, rm -rf, --no-verify) with harness hooks, careful and frozen modes, and prote… |
| [`agent-loops`](skills/agent-loops/SKILL.md) | experimental | Use when designing, running or reviewing an autonomous or long-running agent loop: machine-checkable goals and stop conditions, quality gates and evals inside the loop, operator approval points, recovery, and failure mo… |
| [`agent-memory`](skills/agent-memory/SKILL.md) | experimental | Use when an agent should learn across sessions: capturing durable lessons and decisions, promoting observations into rules or skills, pruning stale memory, keeping a scoped context file, and distilling repeated correcti… |
| [`agent-teams`](skills/agent-teams/SKILL.md) | experimental | Use when coordinating several agents as a team on one effort: assigning owners and scope to work items, isolating each agent in its own branch or worktree, tracking state on a board, merge gates, and splitting a plan in… |
| [`context-management`](skills/context-management/SKILL.md) | experimental | Use when an agent session is long, expensive or near its context limit: budgeting tokens, deciding when and how to compact, what to keep in context versus files, and estimating the token cost of a task before running it. |
| [`harness-design`](skills/harness-design/SKILL.md) | experimental | Use when designing or auditing an AI agent or agentic product: its tools and action space, observation formatting, permissions, identity and trust, multi-agent topology, and the twelve-layer audit for wrapper regression… |
| [`parallel-agents`](skills/parallel-agents/SKILL.md) | experimental | Use when facing two or more independent tasks (separate failures, subsystems or research questions) that share no state and can run at the same time. Dispatches one focused subagent per task with exactly the context it… |
| [`session-retrospective`](skills/session-retrospective/SKILL.md) | experimental | Use when the user asks for a retrospective on a coding-agent session. Reads the session record and proposes ranked improvements to the agent's environment: navigation pointers, automated checks, review standards, AGENTS… |
| [`skill-authoring`](skills/skill-authoring/SKILL.md) | experimental | Use when creating a new skill, editing or improving an existing one, testing whether a skill triggers and works, benchmarking it against a baseline, or tuning its description so it fires at the right time. Covers intent… |

## Origem e manutenção

- Entrada editorial: [manifesto de `agent-engineering`](../../catalog/curation/domains/agent-engineering.yaml).
- Requisitos: [spec do domínio](../../docs/specs/agent-engineering/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/agent-engineering/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `agent-debugging` | affaan-m/ECC |
| `agent-evaluation` | affaan-m/ECC, davila7/claude-code-templates, github/awesome-copilot, wshobson/agents |
| `agent-guardrails` | affaan-m/ECC, github/awesome-copilot, mattpocock/skills, wshobson/agents |
| `agent-loops` | affaan-m/ECC |
| `agent-memory` | affaan-m/ECC, davila7/claude-code-templates, github/awesome-copilot, wshobson/agents |
| `agent-teams` | VoltAgent/awesome-claude-code-subagents, affaan-m/ECC, wshobson/agents |
| `context-management` | affaan-m/ECC, github/awesome-copilot |
| `harness-design` | affaan-m/ECC, github/awesome-copilot, msitarzewski/agency-agents |
| `parallel-agents` | obra/superpowers |
| `session-retrospective` | mattpocock/skills |
| `skill-authoring` | affaan-m/ECC, anthropics/skills, mattpocock/skills, obra/superpowers |
