# Plano — `code-quality`

## Como os artefatos são produzidos

Gerados (não editar à mão em `domains/`; editar a fonte e regenerar):

- [manifesto editorial](../../../../catalog/curation/domains/code-quality.yaml) → `python -m tools.curation <sources> --domain code-quality`

Portados com `tools.curation.port` e editados à mão (diff revisável contra o upstream; proveniência em `catalog/curation/domains/code-quality.yaml`):

- `code-quality/code-review`
- `code-quality/code-reviewer`
- `code-quality/codebase-audit`
- `code-quality/debt-ledger`
- `code-quality/receiving-code-review`

## Contratos

- Registro: `catalog/catalog.yaml` (derivado de `catalog/curation/domains/*.yaml` por `python -m tools.catalog rebuild`).
- Proveniência: `domains/code-quality/PROVENANCE.yaml`.
- Correções locais em arquivos gerados: `catalog/overrides/<domínio>/<skill>/`, aplicadas após cada regeneração.

## Decisões

- Base e referências de cada artefato: ver a tabela da [spec](spec.md).
- Referências do upstream são reescritas para artefatos do catálogo; links para arquivos não copiados viram texto; seções de persona são removidas.

## Verificação

- `python -m tools.validate` (formato, catálogo, nomes, similaridade, licença, higiene, links).
- `python -m tools.evals.triggers --routing` (pago; requer `ANTHROPIC_API_KEY`).
