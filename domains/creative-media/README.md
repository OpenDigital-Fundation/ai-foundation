# `creative-media`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

Visual pieces and media - banners, slides, generative art, GIFs, images.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install creative-media@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`animated-gifs`](skills/animated-gifs/SKILL.md) | experimental | Use when making an animated GIF, especially for Slack or chat: size and frame limits, animation concepts, generation with Python and validation of the result. |
| [`banner-design`](skills/banner-design/SKILL.md) | experimental | Use when designing banners and promotional graphics: social media posts and covers, display ads, website heroes and print, with several art directions to choose from and platform-correct sizes. |
| [`generative-art`](skills/generative-art/SKILL.md) | experimental | Use when the user asks for art made with code: generative or algorithmic art in p5.js with seeded randomness, flow fields, particle systems and interactive parameters. |
| [`image-prompting`](skills/image-prompting/SKILL.md) | experimental | Use when writing prompts for image-generation models: photographic direction (lens, light, composition), style control, and representation that avoids stereotyped or culturally inaccurate depictions of people. |
| [`poster-design`](skills/poster-design/SKILL.md) | experimental | Use when creating a static visual piece as a PNG or PDF: a poster, cover, print piece or art board composed from a written design philosophy, with bundled typefaces. |
| [`presentation-slides`](skills/presentation-slides/SKILL.md) | experimental | Use when creating an HTML slide deck or presentation from scratch or from an outline: narrative structure, slide layouts, animation, charts with Chart.js and design tokens, or converting an existing deck to HTML. For .p… |

## Origem e manutenção

- Entrada editorial: [manifesto de `creative-media`](../../catalog/curation/domains/creative-media.yaml).
- Requisitos: [spec do domínio](../../docs/specs/creative-media/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/creative-media/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `animated-gifs` | anthropics/skills |
| `banner-design` | nextlevelbuilder/ui-ux-pro-max-skill |
| `generative-art` | anthropics/skills, davila7/claude-code-templates |
| `image-prompting` | github/awesome-copilot, msitarzewski/agency-agents |
| `poster-design` | anthropics/skills |
| `presentation-slides` | affaan-m/ECC, msitarzewski/agency-agents, nextlevelbuilder/ui-ux-pro-max-skill |
