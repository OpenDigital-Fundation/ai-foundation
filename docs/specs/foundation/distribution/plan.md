# Plano — Distribuição

## Arquitetura

```
.claude-plugin/marketplace.json      # gerado a partir de catalog.yaml e profiles/
profiles/<perfil>.yaml
tools/build/
  marketplace.py                     # R1, R5
  adapters/{codex,cursor,gemini,opencode,copilot}.py   # R3
.github/workflows/release.yml        # build + anexos da release
.github/workflows/upstream-sync.yml  # R7, semanal
```

## Contratos

```yaml
# profiles/fullstack-web.yaml
name: fullstack-web
description: Daily engineering loop for a TypeScript web product.
include:
  - principles/*
  - workflow/*
  - testing/test-driven-development
  - code-quality/code-review
  - debugging/systematic-debugging
  - languages/typescript
  - ui/visual-design
  - ux/usability-heuristics
  - accessibility/accessibility-audit
```

Profiles iniciais: `fullstack-web`, `backend-service`, `security-review`, `agent-builder`, `product-team`, `design-team`.

## Decisões

- Fonte única no formato Claude Code/Agent Skills; os demais são projeções ([ADR generated-harness-adapters](../../../adr/foundation/generated-harness-adapters.md)).
- Snapshot fixado + issue de diff, sem submódulos ([ADR pinned-upstream-snapshots](../../../adr/foundation/pinned-upstream-snapshots.md)).

## Riscos

- Harnesses mudam formato com frequência. Mitigação: um adaptador por harness, com teste de snapshot da saída.
- Skills que dependem de ferramentas do Claude Code (subagentes, hooks). Mitigação: `metadata.requires` no frontmatter; o adaptador omite ou degrada com aviso.
