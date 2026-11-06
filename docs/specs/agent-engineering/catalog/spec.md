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
