# `marketing`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

SEO and answer-engine optimisation, content, social, email, paid media.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install marketing@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`campaign-planning`](skills/campaign-planning/SKILL.md) | experimental | Use when planning a marketing campaign or launch end to end: goals, audience, positioning and messaging, channel mix, calendar, growth experiments, press and communications, and success metrics. |
| [`content-marketing`](skills/content-marketing/SKILL.md) | experimental | Use when planning or producing marketing content: content strategy and calendars, articles and newsletters, LinkedIn and social posts, cross-posting across platforms, developer relations content and community building. |
| [`email-marketing`](skills/email-marketing/SKILL.md) | experimental | Use when planning or writing marketing email: lifecycle and nurture sequences, newsletters, segmentation, deliverability, subject lines and A/B tests, and operating email tools. |
| [`paid-media`](skills/paid-media/SKILL.md) | experimental | Use for paid acquisition: search (PPC) and paid social campaigns, programmatic and display buying, search-query mining, ad creative, conversion tracking and attribution, and auditing ad accounts. |
| [`seo`](skills/seo/SKILL.md) | experimental | Use for search visibility: technical SEO audits, keyword and intent research, on-page optimisation, structured data, Core Web Vitals, answer-engine and AI-citation optimisation, and app store optimisation. |

## Origem e manutenção

- Entrada editorial: [manifesto de `marketing`](../../catalog/curation/domains/marketing.yaml).
- Requisitos: [spec do domínio](../../docs/specs/marketing/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/marketing/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `campaign-planning` | affaan-m/ECC, msitarzewski/agency-agents |
| `content-marketing` | affaan-m/ECC, msitarzewski/agency-agents |
| `email-marketing` | affaan-m/ECC, msitarzewski/agency-agents |
| `paid-media` | msitarzewski/agency-agents |
| `seo` | affaan-m/ECC, msitarzewski/agency-agents |
