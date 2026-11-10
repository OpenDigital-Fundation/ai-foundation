# `accessibility`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

Accessibility conformance and audits - WCAG, ARIA, assistive technology.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install accessibility@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`accessibility-audit`](skills/accessibility-audit/SKILL.md) | experimental | Use when the user asks for an accessibility audit of a website or web app, a conformance or compliance report (Section 508, EN 301 549, EAA, ADA, AODA, VPAT), an accessibility statement, accessibility checks in CI, regr… |
| [`assistive-technology-testing`](skills/assistive-technology-testing/SKILL.md) | experimental | Use when deciding how to test accessibility or running the tests: screen readers (NVDA, JAWS, VoiceOver, Narrator, TalkBack), keyboard-only passes, simulated narration of HTML or JSX, desktop accessibility APIs, automat… |
| [`document-accessibility`](skills/document-accessibility/SKILL.md) | experimental | Use when Word, Excel, PowerPoint, PDF, ePub or Markdown files must be accessible: auditing them one by one or as a folder inventory, fixing titles, headings, reading order, tags, alt text and table headers, PDF/UA and E… |
| [`wcag-accessibility`](skills/wcag-accessibility/SKILL.md) | experimental | Use when designing, building or reviewing interfaces for accessibility on web, mobile or desktop: WCAG 2.2 AA (and AAA or WCAG 3 when asked), semantic roles and ARIA, keyboard and focus, forms and errors, dialogs, contr… |

## Origem e manutenção

- Entrada editorial: [manifesto de `accessibility`](../../catalog/curation/domains/accessibility.yaml).
- Requisitos: [spec do domínio](../../docs/specs/accessibility/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/accessibility/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `accessibility-audit` | Community-Access/accessibility-agents, msitarzewski/agency-agents |
| `assistive-technology-testing` | Community-Access/accessibility-agents, github/awesome-copilot, wshobson/agents |
| `document-accessibility` | Community-Access/accessibility-agents, github/awesome-copilot |
| `wcag-accessibility` | Community-Access/accessibility-agents, affaan-m/ECC, github/awesome-copilot |
