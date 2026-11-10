# Tarefas — Distribuição

- [x] **T1.** `marketplace.py` gera `marketplace.json` com 25 domínios. Verificar: critério de aceite 1 em sessão limpa.
- [x] **T2.** Schema e loader de `profiles/`; criar os 6 profiles iniciais. Verificar: critério 2.
- [x] **T3.** Adaptador Codex/Copilot CLI/Gemini: layout Agent Skills em `dist/agent-skills/` (lido de `~/.agents/skills/`), com teste.
- [x] **T4.** Adaptador Cursor: `.cursor/rules/*.mdc` (princípios com `alwaysApply`), links apontando para as skills instaladas, com teste.
- [x] **T5.** Extensão Gemini CLI: `gemini-extension.json`, `GEMINI.md` e um comando `.toml` por skill, com teste que parseia o TOML.
- [x] **T6.** OpenCode: `.opencode/skills/` + `AGENTS.md` índice. Copilot CLI usa o layout Agent Skills de T3.
- [x] **T7.** `release.yml`: em tag `v*.*.*`, testa, valida, gera os quatro pacotes e publica a release com notas geradas.
- [x] **T8.** `tools.inventory.sync_report` + `upstream-sync.yml` semanal: fontes que andaram, artefatos novos/removidos/alterados e arquivos derivados (via PROVENANCE) que mudaram; abre issue, nunca altera conteúdo. Verificado localmente em 2026-11-06 (ECC e anthropics/skills andaram; nenhum arquivo derivado mudou).
- [ ] **T9.** Verificar cada pacote num harness real (Codex, Cursor, Gemini CLI, OpenCode): carregamento e gatilho de uma skill-piloto.
