# Spec — Catálogo do domínio `agent-engineering`

- **Domínio:** agent-engineering
- **Status:** parcial (Onda 1)
- **Fronteira:** configurar e operar agentes de código — autoria de skills, harness, orquestração, subagentes, loops, memória, contexto.

## Resultado

| Artefato | Base | Fundidos |
|---|---|---|
| `skill-authoring` | Anthropic `skill-creator` (Apache-2.0, aviso de modificação e `LICENSE.txt` mantidos) | superpowers `writing-skills` (em `pressure-testing/`), mattpocock `writing-for-agents` (em `references/`), ECC `skill-create`, `skill-stocktake`, `skill-comply`, `skill-health`; regras de colocação no catálogo |
| `parallel-agents` | superpowers `dispatching-parallel-agents` | — |
| `session-retrospective` | mattpocock `retro` | — |

`using-superpowers` foi excluído: força a invocação de skills antes de qualquer resposta, o que conflita com a regra "usuário > `AGENTS.md` > skill" ([ADR process-discipline-baseline](../../../adr/workflow/process-discipline-baseline.md)).

## Próximos artefatos (ainda não implementados)

O ECC concentra ~160 itens neste domínio (loops, harness, memória, custo, orquestração de equipes de agents, hooks). Antes de portar, cada um precisa passar pelo critério "existe gatilho distinto?". Candidatos: `context-budget`/`strategic-compact`, `agent-harness-construction`, `loop-design-check`, `agent-introspection-debugging`, `prompt-caching-strategy` (→ `ai-engineering`), hooks de guardrail (mattpocock `git-guardrails-claude-code`, ECC `safety-guard`, `gateguard`).

## Segunda passada (bundle [`agent-engineering.yaml`](../../../../catalog/decisions/bundles/agent-engineering.yaml))

| Artefato | Base | Referências |
|---|---|---|
| `context-management` | ECC `context-budget` | `strategic-compact`, `token-budget-advisor` |
| `harness-design` | ECC `agent-harness-construction` | `agent-architecture-audit`, `agentic-engineering`, `ai-first-engineering`, `enterprise-agent-ops`, agent `harness-optimizer`; agency *Multi-Agent Systems Architect*, *Agents Orchestrator*, *Agentic Identity & Trust Architect* |
| `agent-loops` | ECC `loop-design-check` | `autonomous-loops`, `continuous-agent-loop`, `operator-approval-loop`, `autonomous-agent-harness`, agent `loop-operator` |
| `agent-evaluation` | ECC `agent-eval` | `eval-harness`, `agent-self-evaluation`, `benchmark-optimization-loop`, agent `agent-evaluator` |
| `agent-debugging` | ECC `agent-introspection-debugging` | agent `conversation-analyzer` |
| `agent-guardrails` | mattpocock `git-guardrails-claude-code` | ECC `safety-guard` (hooks opt-in, instalados só com aprovação) |
| `agent-teams` | ECC `team-agent-orchestration` | `team-builder`, `plan-orchestrate`, `parallel-execution-optimizer`; absorve `multi-*`, `claude-devfleet`, `dev-team` |
| `agent-memory` | ECC `continuous-learning-v2` | `continuous-learning`, `unified-memory`, `context-and-decisions`, `rules-distill`, agent `observer`; absorve `learn*`, `instinct-*`, `evolve`, `promote`, `prune` |

Os ~86 hooks das fontes (runtime de hooks do ECC, rastreamento de modo do ponytail, injeção de sessão do superpowers) foram excluídos como `source-internal`; guardrails entram por `agent-guardrails`, opt-in. Mapeamentos de itens soltos para artefatos existentes estão em [`remaining-mappings.yaml`](../../../../catalog/decisions/remaining-mappings.yaml) (seção `extend`).
