# Spec — Catálogo do domínio `marketing`

- **Domínio:** marketing
- **Status:** em implementação (Onda 3)
- **Fronteira:** SEO/AEO, conteúdo, social, e-mail, mídia paga.

## Resultado (gerado por `tools.curation.bundle` a partir de [`bundles/business.yaml`](../../../../catalog/decisions/bundles/business.yaml))

| Artefato | Base | Referências |
|---|---|---|
| `seo` | `seo` | `seo-specialist`, `seo-specialist`, `aeo-foundations`, `ai-citation-strategist`, `agentic-search-optimizer`, `app-store-optimizer` |
| `content-marketing` | `content-engine` | `article-writing`, `content-creator`, `linkedin-content-creator`, `social-media-strategist`, `crosspost`, `developer-advocate`, `developer-community-builder` |
| `email-marketing` | `email-strategist` | `email-ops` |
| `paid-media` | `ppc-strategist` | `paid-social-strategist`, `programmatic-buyer`, `search-query-analyst`, `auditor`, `creative-strategist`, `tracking-specialist` |
| `campaign-planning` | `campaign` | `growth-hacker`, `pr-communications-manager` |

## Notas

- Base em personas do agency-agents: o texto é persona, não procedimento verificável. Revisar cada skill e reescrever o corpo como passos com critério de saída antes de promover a `stable`.
- Plataformas regionais (Douyin, Xiaohongshu, Weibo, Bilibili, Zhihu, Baidu, WeChat, Kuaishou) e e-commerce transfronteiriço ficam fora de escopo v1.
