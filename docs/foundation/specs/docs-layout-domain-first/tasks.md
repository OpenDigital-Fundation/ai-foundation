# Tarefas — Layout de specs e ADRs por domínio

Plano: [plan.md](plan.md). Spec: [spec.md](spec.md).

- [x] T1. ADR `2026-11-21-docs-layout-domain-first` e status "substituído" no ADR antigo.
- [x] T2. `check_docs_layout` em `tools/validate/checks.py`, ligado a `run_all`.
- [x] T3. Testes do validador em `tools/validate/test_checks.py`.
- [x] T4. `tools/build/docs.py` resolve a spec do domínio nos dois layouts; `tools/build/test_docs.py` cobre os dois.
- [x] T5. `AGENTS.md` (Layout e Convenções), `docs/architecture/repository-layout.md`, `docs/README.md`, `README.md`.
- [x] T6. Padrões e modelos das skills e `catalog/renames.yaml`.
- [x] T7. `uv run python -m tools.validate` e `uv run pytest -q`.
