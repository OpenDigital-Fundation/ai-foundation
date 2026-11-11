# ROADMAP — OpenDigital AI Foundation

Lista as specs filhas, a ordem e as dependências. Sem requisitos nem tarefas: cada spec tem o próprio ciclo spec → plano → implementação → revisão.

## Onda 0 — Fundação (bloqueia todo o resto)

| Spec | Depende de | Entrega |
|---|---|---|
| [`foundation/catalog-governance`](foundation/catalog-governance/spec.md) | — | Taxonomia de domínios, regra de unicidade, tipos de artefato, nomes, `catalog.yaml` |
| [`foundation/source-curation`](foundation/source-curation/spec.md) | catalog-governance | Inventário das fontes, `sources.lock.yaml`, matriz manter/fundir/descartar, proveniência |
| [`foundation/quality-gates`](foundation/quality-gates/spec.md) | catalog-governance | Validadores de CI, detecção de duplicata, evals |
| [`foundation/distribution`](foundation/distribution/spec.md) | catalog-governance, quality-gates | Marketplace de plugins por domínio e adaptadores multi-harness |
| [`foundation/source-expansion`](foundation/source-expansion/spec.md) | source-curation | Fontes novas em quatro fatias (oficiais, awesome-copilot, grandes coleções, ciência) |
| [`foundation/faceted-classification`](foundation/faceted-classification/spec.md) | catalog-governance | Facetas N:N (tecnologia, conhecimento, capacidade, setor, áreas multidisciplinares) sobre a posse por domínio |

## Revisão da organização do repositório

| Spec | Depende de |
|---|---|
| [`foundation/curation-layout`](foundation/curation-layout/spec.md) | catalog-governance, source-curation |
| [`foundation/artifact-support-layout`](foundation/artifact-support-layout/spec.md) | curation-layout |
| [`foundation/repository-guide`](foundation/repository-guide/spec.md) | curation-layout, artifact-support-layout |

## Onda 1 — Núcleo de engenharia (uso diário)

| Spec | Depende de |
|---|---|
| [`principles/catalog`](principles/catalog/spec.md) | Onda 0 |
| [`workflow/catalog`](workflow/catalog/spec.md) | principles |
| [`testing/catalog`](testing/catalog/spec.md) | principles |
| [`debugging/catalog`](debugging/catalog/spec.md) | testing |
| [`code-quality/catalog`](code-quality/catalog/spec.md) | principles, testing |
| [`architecture/catalog`](architecture/catalog/spec.md) | workflow |
| [`security/catalog`](security/catalog/spec.md) | code-quality |
| [`agent-engineering/catalog`](agent-engineering/catalog/spec.md) | quality-gates |

## Onda 2 — Stack e produto digital

| Spec | Depende de |
|---|---|
| [`languages/catalog`](languages/catalog/spec.md) | testing, code-quality, debugging |
| [`ui/catalog`](ui/catalog/spec.md) | accessibility |
| [`ux/catalog`](ux/catalog/spec.md) | — |
| [`accessibility/catalog`](accessibility/catalog/spec.md) | — |
| [`brand/catalog`](brand/catalog/spec.md) | ui |
| [`creative-media/catalog`](creative-media/catalog/spec.md) | brand |
| [`data/catalog`](data/catalog/spec.md) | languages |
| [`ai-engineering/catalog`](ai-engineering/catalog/spec.md) | agent-engineering |
| [`platform/catalog`](platform/catalog/spec.md) | security |
| [`documents/catalog`](documents/catalog/spec.md) | — |
| [`research/catalog`](research/catalog/spec.md) | — |
| [`science/catalog`](science/catalog/spec.md) | research, foundation/source-expansion (fatia 4) |

## Onda 3 — Negócio

| Spec | Depende de |
|---|---|
| [`product/catalog`](product/catalog/spec.md) | workflow, research |
| [`marketing/catalog`](marketing/catalog/spec.md) | brand |
| [`sales/catalog`](sales/catalog/spec.md) | — |
| [`finance/catalog`](finance/catalog/spec.md) | — |
| [`legal-compliance/catalog`](legal-compliance/catalog/spec.md) | security |
| [`operations/catalog`](operations/catalog/spec.md) | — |

## Fora de escopo nesta versão

Nichos verticais (games, GIS, XR, saúde, cripto/DeFi, homelab/redes, logística, plataformas chinesas, CMSs específicos) e ferramentas internas das próprias fontes (`ecc-*`, `ponytail-gain`, `ask-matt`...). Registrados em `catalog/exclusions.yaml`; reabrir exige uma spec nova de domínio.

## Fora deste repositório

- **`opendigital-ai-landscape`** — registro de recursos externos (repositórios, modelos, datasets, MCPs, frameworks) classificados pelas mesmas facetas. Produto e repositório próprios; consome `catalog/taxonomy/` como contrato ([ADR faceted-classification](../adr/foundation/faceted-classification.md)).
