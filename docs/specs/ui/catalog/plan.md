# Plano — `ui`

## Como os artefatos são produzidos

Gerados (não editar à mão em `domains/`; editar a fonte e regenerar):

- [manifesto editorial](../../../../catalog/curation/domains/ui.yaml) → `python -m tools.curation <sources> --domain ui`

Portados com `tools.curation.port` e editados à mão (diff revisável contra o upstream; proveniência em `catalog/curation/domains/ui.yaml`):

- `ui/design-system`
- `ui/visual-design`

## Contratos

- Registro: `catalog/catalog.yaml` (derivado de `catalog/curation/domains/*.yaml` por `python -m tools.catalog rebuild`).
- Proveniência: `domains/ui/PROVENANCE.yaml`.
- Correções locais em arquivos gerados: `catalog/overrides/<domínio>/<skill>/`, aplicadas após cada regeneração.

## Decisões

- Base e referências de cada artefato: ver a tabela da [spec](spec.md).
- Referências do upstream são reescritas para artefatos do catálogo; links para arquivos não copiados viram texto; seções de persona são removidas.

## Verificação

- `python -m tools.validate` (formato, catálogo, nomes, similaridade, licença, higiene, links).
- `python -m tools.evals.triggers --routing` (pago; requer `ANTHROPIC_API_KEY`).
