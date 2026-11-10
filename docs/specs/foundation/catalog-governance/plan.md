# Plano — Governança do catálogo

## Arquitetura

```
domains/<domínio>/.claude-plugin/plugin.json
catalog/curation/domains/   # fonte editorial dos registros e receitas
catalog/catalog.yaml        # projeção gerada do que existe
catalog/curation/exclusions.yaml  # fonte editorial do que não entra
catalog/exclusions.yaml     # projeção gerada das exclusões
catalog/schema/*.json       # JSON Schema dos três arquivos de catálogo e do frontmatter
catalog/naming.yaml         # termos proibidos em nomes (marcas, superlativos)
```

## Contratos

### `catalog.yaml`

```yaml
version: 1
artifacts:
  - id: testing/test-driven-development
    type: skill            # skill | agent | workflow | prompt | rule | hook | mcp | template | knowledge | profile
    capability: "Write a failing test first, then the minimum code to pass, then refactor."
    status: experimental   # experimental | stable | deprecated
    owner: "@opendigital/ai-foundation"
    supersedes:            # chaves do inventário upstream (source:kind:name)
      - obra/superpowers:skill:test-driven-development
      - mattpocock/skills:skill:tdd
      - affaan-m/ECC:skill:tdd-workflow
```

### `exclusions.yaml`

```yaml
version: 1
excluded:
  - key: nextlevelbuilder/ui-ux-pro-max-skill:skill:ui-ux-pro-max
    reason: split            # duplicate-of | split | out-of-scope | license | source-internal | low-quality | vendor-specific
    into: [ui/visual-design, ux/usability-heuristics, accessibility/accessibility-audit]
```

### Frontmatter de skill (padrão Agent Skills + metadados próprios)

```yaml
---
name: test-driven-development
description: Use when implementing a feature or fixing a bug, before writing implementation code. ...
license: MIT
metadata:
  domain: testing
  status: experimental
---
```

## Decisões

- Domínio = plugin ([ADR domain-first-layout](../../../adr/foundation/domain-first-layout.md)): o usuário instala só o que usa e o namespace evita colisão.
- Unicidade decidida por gatilho, não por nome ([ADR one-capability-per-domain](../../../adr/foundation/one-capability-per-domain.md)).
- Chave do inventário `source:kind:name` é estável entre atualizações upstream porque o caminho muda mais que o nome.

## Riscos

- **Fronteira ambígua entre domínios** (ex.: review de segurança é `security` ou `code-quality`?). Mitigação: a frase de fronteira de R1 decide; o caso vira exemplo na própria tabela.
- **Fusão perde qualidade das fontes.** Mitigação: evals comparam a skill fundida com a melhor fonte (spec `quality-gates`).
