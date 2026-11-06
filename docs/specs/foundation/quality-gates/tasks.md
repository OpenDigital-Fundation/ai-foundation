# Tarefas — Portões de qualidade

- [x] **T1.** `schema.py` + testes (fixtures válidas e inválidas). Verificar: `pytest tools/validate`.
- [x] **T2.** `names.py` com `naming.yaml`. Verificar: critério de aceite 1.
- [ ] **T3.** Calibrar `similarity.py` com 20 pares rotulados do inventário (10 duplicatas, 10 distintos); escolher o limiar. Verificar: critério 2 e relatório de precisão/recall no PR.
- [x] **T4.** `license.py` usando hashes gerados pelo `fetch.sh`. Verificar: critério 3.
- [x] **T5.** `hygiene.py` (gitleaks, padrões de telemetria/autopromoção, MCP com versão fixa).
- [x] **T6.** Workflow `validate.yml`. Verificar: critério 5 (tempo).
- [ ] **T7.** `run_triggers.py` e `run_tasks.py` com uma skill-piloto (`testing/test-driven-development`).
- [ ] **T8.** `evals/routing/` com 50 prompts cobrindo os domínios da Onda 1.
- [ ] **T9.** Workflow `evals.yml` (label, promoção, semanal).
