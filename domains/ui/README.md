# `ui`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

Visual interface - aesthetic direction, typography, colour, layout, tokens, design systems, components, finish.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install ui@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`component-styling`](skills/component-styling/SKILL.md) | experimental | Use when implementing interface components and styles in code: shadcn/ui and Radix components, Tailwind utility styling, theming and dark mode, responsive layouts, CSS architecture, and applying a ready-made theme to an… |
| [`design-system`](skills/design-system/SKILL.md) | experimental | Use when choosing or generating a design system for a product: visual style, colour palette, font pairing, chart types, icons, landing-page structure and stack-specific UI guidelines. Searches a curated database by prod… |
| [`motion-and-polish`](skills/motion-and-polish/SKILL.md) | experimental | Use when an interface works but feels flat or rough: adding purposeful motion and transitions, micro-interactions, easing and timing, reduced-motion support, and the small craft details that make an interface feel consi… |
| [`visual-design`](skills/visual-design/SKILL.md) | experimental | Use when the user asks to design or build a new website, landing page or page that must look designed rather than generated. Deals themes, builds the page around the visitor's job, and lints the result in a real browser… |

## Origem e manutenção

- Entrada editorial: [manifesto de `ui`](../../catalog/curation/domains/ui.yaml).
- Requisitos: [spec do domínio](../../docs/specs/ui/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/ui/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `component-styling` | anthropics/skills, github/awesome-copilot, msitarzewski/agency-agents, nextlevelbuilder/ui-ux-pro-max-skill |
| `design-system` | affaan-m/ECC, msitarzewski/agency-agents, nextlevelbuilder/ui-ux-pro-max-skill |
| `motion-and-polish` | affaan-m/ECC, msitarzewski/agency-agents |
| `visual-design` | Nutlope/hallmark, affaan-m/ECC, anthropics/skills, github/awesome-copilot, msitarzewski/agency-agents, nextlevelbuilder/ui-ux-pro-max-skill |
