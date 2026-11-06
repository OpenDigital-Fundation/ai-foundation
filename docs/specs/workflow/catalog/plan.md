# Plano — `workflow`

- Port mecânico com `tools/curation/port.py` (renomes em `catalog/renames.yaml`), seguido de edição manual revisável como diff contra o upstream.
- `executing-plans`: `SKILL.md` roteador + `modes/inline.md` + `modes/subagent.md`; `scripts/`, `prompts/` e `references/` compartilhados; `PLAN_FILE` = `tasks.md`.
- `writing-plans`: `plan.md` (cabeçalho, restrições globais, arquivos, foco de revisão) e `tasks.md` (`### Task N`, formato que os scripts de execução analisam).
- `feature-delivery` em `workflows/feature-delivery/SKILL.md`, carregado pelo `plugin.json` com `skills: ["./skills/", "./workflows/"]`.
- Decisões em `catalog/decisions/workflow.yaml`, aplicadas com `python -m tools.catalog apply`.
