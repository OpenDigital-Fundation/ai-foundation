# ROADMAP — OpenDigital AI Foundation

Lista as specs filhas, a ordem e as dependências. Sem requisitos nem tarefas: cada spec tem o próprio ciclo spec → plano → implementação → revisão.

## Onda 0 — Fundação (bloqueia todo o resto)

| Spec | Depende de | Entrega |
|---|---|---|
| [`foundation/catalog-governance`](foundation/catalog-governance/spec.md) | — | Taxonomia de domínios, regra de unicidade, tipos de artefato, nomes, `catalog.yaml` |
| [`foundation/source-curation`](foundation/source-curation/spec.md) | catalog-governance | Inventário das fontes, `sources.lock.yaml`, matriz manter/fundir/descartar, proveniência |
| [`foundation/quality-gates`](foundation/quality-gates/spec.md) | catalog-governance | Validadores de CI, detecção de duplicata, evals |
| [`foundation/distribution`](foundation/distribution/spec.md) | catalog-governance, quality-gates | Marketplace de plugins por domínio e adaptadores multi-harness |

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

## Estado das specs

| Spec | Estado |
|---|---|
| `foundation/catalog-governance` | implementada (falta T6: revisão humana da tabela de domínios) |
| `foundation/source-curation` | implementada; 100% do inventário decidido (verificado no CI) |
| `foundation/quality-gates` | validação estática implementada; faltam calibração do limiar (T3), runner de evals (T7–T9) |
| `foundation/distribution` | marketplace, profiles, adaptadores (Agent Skills, Cursor, Gemini, OpenCode) e release implementados; faltam sync upstream (T8) e verificação em harness real (T9) |
| `principles`, `workflow`, `testing`, `debugging`, `code-quality` | primeira versão implementada (`experimental`); faltam evals |
| `agent-engineering` | parcial: `parallel-agents`, `writing-skills`, `session-retrospective` portados; fusão com `skill-creator` pendente |
| `architecture`, `security` | primeira versão implementada (`experimental`); faltam evals |
| `languages` | 11 pacotes gerados (`experimental`); faltam revisão de conteúdo e evals |
| `ui`, `ux`, `accessibility` | primeira versão (`experimental`); faltam evals e testes dos scripts do upstream |
| `data`, `platform`, `ai-engineering`, `documents`, `research`, `brand`, `creative-media` | primeira versão via `tools.curation.bundle` (`experimental`) |
| Onda 3 (`product`, `marketing`, `sales`, `finance`, `legal-compliance`, `operations`) | primeira versão via bundle (`experimental`); corpos baseados em personas precisam virar procedimentos |
