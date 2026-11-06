# Spec — Catálogo do domínio `workflow`

- **Domínio:** workflow
- **Status:** em implementação
- **ADR:** [process-discipline-baseline](../../../adr/workflow/process-discipline-baseline.md)
- **Fronteira:** ciclo de entrega — ideação, spec, plano, execução, worktrees, conclusão de branch, handoff, tickets.

## Problema

Três fontes cobrem o ciclo de entrega com ~60 artefatos sobrepostos: superpowers (processo com portões), mattpocock (skills curtas de interrogação, spec, tickets, handoff) e ECC (famílias `prp-*`, `orch-*`, `epic-*`, comandos `plan`, `feature-dev`). Os nomes diferem, os gatilhos colidem e cada família assume seu próprio layout de documentos.

## Resultado

| Artefato | Tipo | Base | Fundidos |
|---|---|---|---|
| `brainstorming` | skill | superpowers | mattpocock `to-spec` (modo "conversa já resolvida" + template de spec), `prototype` (spike), ECC `plan-prd`/`prp-prd`/`intent-driven-development`, agency *Rapid Prototyper* |
| `grilling` | skill | mattpocock | `grill-me`, `grill-with-docs` |
| `writing-plans` | skill | superpowers | ECC `planner`, `plan`, `prp-plan` |
| `executing-plans` | skill | superpowers `executing-plans` + `subagent-driven-development` (dois modos, mesma infraestrutura) | mattpocock `implement`/`implement-spec`, ECC `prp-implement`, `checkpoint` |
| `git-worktrees` | skill | superpowers | — |
| `finishing-a-branch` | skill | superpowers | ECC `prp-pr`, `prp-commit` |
| `handoff` | skill | skill de handoff da OpenDigital | mattpocock `handoff`/`claude-handoff`, ECC `save-session`/`resume-session` |
| `issue-breakdown` | skill | mattpocock `to-tickets` | ECC `epic-decompose`/`epic-publish`, `story-lifecycle` |
| `initiative-mapping` | skill | mattpocock `wayfinder` | — |
| `issue-triage` | skill | mattpocock `triage` | — |
| `feature-delivery` | workflow | novo | famílias `orch-*` e `feature-dev` do ECC |
| `knowledge/issue-tracking/` | knowledge | mattpocock `setup-matt-pocock-skills` | — |

`retro` do mattpocock foi para `agent-engineering/session-retrospective` (melhora o ambiente do agente, não a entrega). As decisões completas, inclusive exclusões, estão em [`catalog/decisions/workflow.yaml`](../../../../catalog/decisions/workflow.yaml).

## Requisitos

- **R1.** Saídas seguem o layout do `AGENTS.md` do repositório; padrão `docs/specs/<domínio>/<feature>/{spec,plan,tasks}.md`.
- **R2.** Nenhuma skill impõe uso obrigatório global ("você DEVE usar antes de qualquer resposta"); prioridade: usuário > `AGENTS.md` > skill.
- **R3.** Referências entre skills usam `<domínio>:<skill>`.
- **R4.** Skills que publicam em tracker são invocadas só pelo usuário (`disable-model-invocation: true`).
- **R5.** Sem servidores, telemetria ou recursos de marca das fontes (o *visual companion* do superpowers foi retirado: servidor local com logo carregado de URL externa).

## Critérios de aceite

1. Validador sem erros e sem par de skills do domínio com similaridade ≥ 0,80.
2. `feature-delivery` referencia só skills existentes no catálogo.
3. Todo item do inventário que a matriz acima cita tem decisão registrada.

## Pendências de verificação

- Confirmar numa sessão real do Claude Code que `"skills": ["./skills/", "./workflows/"]` no `plugin.json` carrega `feature-delivery`.
- Evals de gatilho e de tarefa por skill (dependem do runner de `quality-gates`).
