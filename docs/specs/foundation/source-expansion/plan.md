# Plano — Expansão de fontes

- Clonar no commit fixado, registrar no lock, regenerar `catalog/inventory/` e ler a distribuição de licenças.
- Mapear itens a artefatos existentes pelo nome e descrição; o que é novo vira receita no manifesto do domínio dono; o resto vira exclusão em `catalog/curation/exclusions.yaml`.
- Reconstruir com `python -m tools.curation <sources-dir> --domain <domínio>`; regenerar catálogo e índices.
