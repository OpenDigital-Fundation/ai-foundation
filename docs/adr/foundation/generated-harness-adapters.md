# Adaptadores de harness gerados
- **Status:** proposto
- **Data:** 2026-11-06
- **Domínio:** foundation

## Contexto

ECC e ponytail mantêm à mão cópias para Cursor, Codex, Gemini, OpenCode, Copilot e outros (`.cursor/`, `.openclaw/`, `pi/`), o que gerou divergência e duplicação interna (1.275 arquivos brutos para 1.007 únicos no inventário).

## Decisão

A fonte única é o layout Claude Code/Agent Skills. Pacotes para outros harnesses são gerados no build da release e não são versionados.

## Consequências

- Uma correção vale para todos os harnesses.
- Cada adaptador precisa de teste de snapshot e acompanhar mudanças de formato do harness.
