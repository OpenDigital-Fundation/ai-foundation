# Tarefas — Portões de qualidade

- [x] **T1.** `schema.py` + testes (fixtures válidas e inválidas). Verificar: `pytest tools/validate`.
- [x] **T2.** `names.py` com `naming.yaml`. Verificar: critério de aceite 1.
- [x] **T3.** Calibrado em 2026-11-06 com 507 descrições do inventário (1.780 pares "fundidos no mesmo artefato", 126.491 pares de artefatos diferentes). Resultado: em 0,80 há zero falsos positivos; pares distintos do mesmo domínio chegam no máximo a 0,63, então o aviso em 0,60 é raro; o recall sobre fusões é ~0 em qualquer limiar útil (4% em 0,30). Limiares mantidos (0,80 bloqueia, 0,60 avisa).
- [ ] **T10.** Detecção semântica de sobreposição: o portão lexical só pega cópias e paráfrases próximas. Medir sobreposição semântica com os evals de roteamento (colisões entre skills) e, se necessário, um modo opcional por embeddings.
- [x] **T4.** `license.py` usando hashes gerados pelo `fetch.sh`. Verificar: critério 3.
- [x] **T5.** `hygiene.py` (gitleaks, padrões de telemetria/autopromoção, MCP com versão fixa).
- [x] **T6.** Workflow `validate.yml`. Verificar: critério 5 (tempo).
- [x] **T7.** Runner de gatilhos (`tools/evals/triggers.py`) com harness isolado; `run_tasks` (rubricas) pendente.
- [x] **T8.** `evals/routing/wave1.yaml` (33 casos; ampliar para 50) com prompts cobrindo os domínios da Onda 1.
- [x] **T9.** Workflow `evals.yml` (label `run-evals` e disparo manual; sem agenda semanal para não gerar custo recorrente sem decisão).
