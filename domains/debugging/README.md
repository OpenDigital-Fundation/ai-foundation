# `debugging`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

Finding the cause of failures - diagnosis, build errors, silent failures.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install debugging@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`build-failure-resolution`](skills/build-failure-resolution/SKILL.md) | experimental | Use when a build, compile, type-check, bundling or dependency step fails, or when errors are being swallowed silently: read the first real error, fix the smallest cause, rebuild, repeat; then hunt for empty catches and… |
| [`systematic-debugging`](skills/systematic-debugging/SKILL.md) | experimental | Use when encountering any bug, test failure, crash, performance regression or unexpected behaviour, before proposing a fix. First builds a tight, deterministic feedback loop that goes red on the exact symptom, then trac… |

## Origem e manutenção

- Entrada editorial: [manifesto de `debugging`](../../catalog/curation/domains/debugging.yaml).
- Requisitos: [spec do domínio](../../docs/specs/debugging/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/debugging/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `build-failure-resolution` | affaan-m/ECC, github/awesome-copilot |
| `systematic-debugging` | github/awesome-copilot, mattpocock/skills, obra/superpowers |
