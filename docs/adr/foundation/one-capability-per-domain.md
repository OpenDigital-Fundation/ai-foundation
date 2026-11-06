# Uma capacidade, um artefato
- **Status:** proposto
- **Data:** 2026-11-06
- **Domínio:** foundation

## Contexto

As fontes repetem a mesma capacidade com nomes diferentes (ex.: `test-driven-development`, `tdd`, `tdd-workflow`, `tdd-guide`, `django-tdd`...). Duplicatas competem pelo gatilho, confundem o roteamento do agente e gastam contexto.

## Decisão

A chave do catálogo é `domínio/capacidade`, e capacidade é definida pelo **gatilho** (quando usar), não pelo nome. Gatilhos sobrepostos no mesmo tipo de artefato são fundidos no melhor candidato, segundo os critérios da spec `source-curation` (licença, verificabilidade, concisão, evals, manutenção). Um artefato que cobre dois domínios é dividido.

## Consequências

- O catálogo fica menor que a soma das fontes (estimativa: de ~1.000 para ~150–250 artefatos).
- Toda decisão fica registrada em `supersedes` ou `exclusions.yaml`, então é auditável.
- A detecção automática (similaridade) é auxiliar; a decisão final é humana na spec do domínio.
