# Spec — Classificação por facetas

- **Domínio:** foundation
- **Status:** em implementação
- **ADR:** [faceted-classification](../../../adr/foundation/faceted-classification.md)
- **Insumo:** taxonomia "OpenDigital AI & Knowledge Landscape v1.0" (seis dimensões, domínios de IA, domínios de conhecimento, famílias de capacidades, grupos setoriais, áreas multidisciplinares).

## Problema

Hoje só se encontra um artefato pelo domínio dono. Não dá para perguntar "o que serve a GovTech", "tudo que pesquisa e cita fontes" ou "o que usa RAG".

## Requisitos

- **R1.** Vocabulários versionados em `catalog/taxonomy/`: `technology.yaml`, `knowledge.yaml`, `capabilities.yaml`, `industries.yaml`, `multidisciplinary.yaml`. Cada termo: `id` estável (inglês, kebab-case), `name.pt`, `name.en`, `parent` opcional, `external` opcional (IPL, ISCED, ESCO, O*NET, ISIC, CNAE).
- **R2.** Termos que vieram da taxonomia-insumo são marcados `origin: landscape-v1`; termos que esta curadoria acrescentou para completar uma lista truncada são `origin: proposed` e ficam para revisão humana.
- **R3.** `catalog/facets.yaml` atribui a cada artefato do catálogo pelo menos um `knowledge` e uma `capabilities`; `technology` e `industries` quando se aplicam.
- **R4.** O validador falha se um artefato não tiver facetas, se uma faceta citar ID inexistente, ou se houver ID duplicado num vocabulário.
- **R5.** Índices gerados navegam por faceta: `docs/FACETS.md` (artefatos por capacidade, conhecimento, tecnologia e setor) e as facetas aparecem no `README.md` de cada domínio.
- **R6.** Nenhum código externo inventado: o campo `external` só é preenchido com código conferido na fonte oficial.

## Critérios de aceite

1. Todos os 111 artefatos com facetas válidas; `python -m tools.validate` sem erros.
2. `docs/FACETS.md` responde "o que serve a GovTech" e "o que faz code review" em uma busca na página.
3. Os vocabulários validam no schema `catalog/schema/taxonomy.schema.json`.

## Fora de escopo

- O registro de recursos externos (`opendigital-ai-landscape`): repositório próprio, spec própria.
- Preencher mapeamentos externos (ESCO, O*NET, CNAE...): tarefa separada, com verificação na fonte.
