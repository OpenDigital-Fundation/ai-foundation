# `brand`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

Brand identity, voice and style guides.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install brand@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`brand-identity`](skills/brand-identity/SKILL.md) | experimental | Use when defining or applying a brand: discovery interviews, positioning, visual identity (logo direction, colour, typography), messaging framework, brand guidelines, asset management and checking content for brand cons… |
| [`brand-voice`](skills/brand-voice/SKILL.md) | experimental | Use when writing should sound like a specific person or company: build a style profile from their real posts, essays, launch notes or docs, then write or edit drafts in that voice and flag lines that break it. |

## Origem e manutenção

- Entrada editorial: [manifesto de `brand`](../../catalog/curation/domains/brand.yaml).
- Requisitos: [spec do domínio](../../docs/specs/brand/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/brand/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `brand-identity` | affaan-m/ECC, msitarzewski/agency-agents, nextlevelbuilder/ui-ux-pro-max-skill |
| `brand-voice` | affaan-m/ECC |
