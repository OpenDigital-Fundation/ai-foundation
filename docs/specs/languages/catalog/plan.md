# Plano — `languages`

## Como os artefatos são produzidos

Gerados (não editar à mão em `domains/`; editar a fonte e regenerar):

- [`catalog/decisions/language-packs.yaml`](../../../../catalog/decisions/language-packs.yaml) → `python -m tools.curation.language_pack <sources> catalog/decisions/language-packs.yaml`

## Contratos

- Registro: `catalog/catalog.yaml` (derivado de `catalog/decisions/*.yaml` por `python -m tools.catalog rebuild`).
- Proveniência: `domains/languages/PROVENANCE.yaml`.
- Correções locais em arquivos gerados: `catalog/overrides/<domínio>/<skill>/`, aplicadas após cada regeneração.

## Decisões

- Base e referências de cada artefato: ver a tabela da [spec](spec.md).
- Referências do upstream são reescritas para artefatos do catálogo; links para arquivos não copiados viram texto; seções de persona são removidas.

## Verificação

- `python -m tools.validate` (formato, catálogo, nomes, similaridade, licença, higiene, links).
- `python -m tools.evals.triggers --routing` (pago; requer `ANTHROPIC_API_KEY`).
