# Formato aberto Agent Skills como fonte única
- **Status:** proposto
- **Data:** 2026-11-06
- **Domínio:** foundation

## Contexto

A especificação Agent Skills (publicada em `anthropics/skills/spec`) é suportada por Claude Code e adotada por outros harnesses. As fontes já a usam, com variações.

## Decisão

Skills seguem a especificação (`SKILL.md` com `name` e `description`, `references/`, `scripts/`, `assets/`), com metadados próprios em `metadata` (`domain`, `status`, `requires`). Agents usam o formato Markdown com frontmatter do Claude Code.

## Consequências

- Compatível com instaladores do ecossistema.
- Extensões próprias ficam isoladas em `metadata`, sem quebrar a especificação.
