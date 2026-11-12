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

## Referências na projeção plana — correção de 2026-11-12

A coleta dos quatro testes existentes de tools/build revelou que security-audit exportava um link para knowledge externo à pasta da skill sem transportar o arquivo. Executing-plans também referencia o agente canônico code-reviewer em outro domínio. No adaptador, copiar somente alvos que discover reconhece como arquivos públicos de tipo knowledge/agent/template para references/catalog-support/<caminho canônico em domains>, reescrevendo links relativos e preservando fragmentos. Documentar a origem canônica em um pequeno mapa do suporte copiado. Não copiar a árvore inteira do domínio nem executar arquivos.

As quatro projeções reutilizam a mesma rotina; Cursor gera seu corpo a partir da entrada já projetada para manter os destinos corretos. Testar portabilidade de conhecimento com âncora, rejeição de alvo arbitrário e o pacote completo. Descrições projetadas devem preservar a fonte, sem pressupor um prefixo inglês que o schema de frontmatter não exige.
