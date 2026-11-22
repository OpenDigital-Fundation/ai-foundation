# Plano — Layout de specs e ADRs por domínio

Spec: [spec.md](spec.md).

## Abordagem

1. Registrar a decisão em ADR que substitui `docs/adr/foundation/docs-layout-by-domain.md`. O ADR antigo só muda o status.
2. Acrescentar `check_docs_layout` a `tools/validate/checks.py` e ligá-lo a `run_all`. A função lê `docs/` sem depender de arquivos que o repositório mínimo dos testes não tem.
3. Cobrir cada regra com testes em `tools/validate/test_checks.py`, usando o repositório mínimo da fixture `repo`.
4. `tools/build/docs.py`: o link "Requisitos" dos READMEs de domínio aponta para `docs/<domínio>/specs/catalog/spec.md` se existir e, senão, para o caminho antigo. Nenhum spec novo existe hoje, então a saída gerada não muda.
5. `tools/build/test_docs.py`: o teste de links inclui `docs/*/specs` e `docs/*/adr`.
6. Atualizar `AGENTS.md`, `docs/architecture/repository-layout.md`, `docs/README.md`, `README.md`, `catalog/renames.yaml` e os padrões das skills `decision-records`, `brainstorming`, `writing-plans`, `code-review`, `feature-delivery`; os arquivos `templates/adr.md` e `templates/spec.md` não citam caminhos e ficam intactos.

## Decisões

- O repositório não tem `domains/*/templates/`; os modelos de spec e ADR vivem em `skills/*/templates/`.
- `docs/architecture/` serve ao contrato do repositório e também ao domínio `architecture`. O validador só examina os subdiretórios `specs/` e `adr/`.
- Contra o ADR antigo, o layout novo põe o domínio antes do tipo de documento e exige data no nome do ADR.

## Riscos

- Skills portadas têm `PROVENANCE.yaml`; editar o padrão de local não muda a origem nem a licença. Conferir `uv run python -m tools.validate`.
- `catalog/renames.yaml` só afeta portes futuros; o conteúdo já portado é editado direto.
