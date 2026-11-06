# Plano — `ux`

## Como os artefatos são produzidos

Portados com `tools.curation.port` e editados à mão (diff revisável contra o upstream; proveniência em `catalog/decisions/provenance-wave1.yaml`):

- `ux/usability-review`
- `ux/user-research`

## Contratos

- Registro: `catalog/catalog.yaml` (derivado de `catalog/decisions/*.yaml` por `python -m tools.catalog rebuild`).
- Proveniência: `domains/ux/PROVENANCE.yaml`.
- Correções locais em arquivos gerados: `catalog/overrides/<domínio>/<skill>/`, aplicadas após cada regeneração.

## Decisões

- Base e referências de cada artefato: ver a tabela da [spec](spec.md).
- Referências do upstream são reescritas para artefatos do catálogo; links para arquivos não copiados viram texto; seções de persona são removidas.

## Verificação

- `python -m tools.validate` (formato, catálogo, nomes, similaridade, licença, higiene, links).
- `python -m tools.evals.triggers --routing` (pago; requer `ANTHROPIC_API_KEY`).
