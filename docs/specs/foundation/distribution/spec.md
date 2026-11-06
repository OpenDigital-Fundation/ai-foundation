# Spec — Distribuição

- **Domínio:** foundation
- **Status:** proposta para revisão
- **Depende de:** [catalog-governance](../catalog-governance/spec.md), [quality-gates](../quality-gates/spec.md)
- **ADRs:** [agent-skills-open-format](../../../adr/foundation/agent-skills-open-format.md), [generated-harness-adapters](../../../adr/foundation/generated-harness-adapters.md), [pinned-upstream-snapshots](../../../adr/foundation/pinned-upstream-snapshots.md)

## Problema

O usuário precisa instalar só os domínios que usa, em vários harnesses, sem manter cópias divergentes do mesmo conteúdo.

## Requisitos

- **R1. Marketplace Claude Code.** `.claude-plugin/marketplace.json` na raiz lista um plugin por domínio (`domains/<d>`) e um por profile.
- **R2. Formato aberto.** Skills seguem a especificação Agent Skills (`SKILL.md` + `references/`, `scripts/`, `assets/`), instaláveis por ferramentas compatíveis (ex.: `npx skills add`).
- **R3. Adaptadores gerados.** `tools/build/` gera, a partir da mesma fonte, os pacotes de: Codex (skills + `AGENTS.md`), Cursor (rules `.mdc`), Gemini CLI (extensão + comandos `.toml`), OpenCode e GitHub Copilot. Saída só nos artefatos de release, nunca versionada.
- **R4. Workflows e prompts.** Workflows publicam como skills invocáveis; prompts e templates vão como `assets/` das skills que os usam.
- **R5. Profiles.** Instalar um profile instala os plugins de domínio necessários e ativa só os artefatos listados.
- **R6. Versionamento.** SemVer por domínio; release do repositório agrega. Changelog gerado de Conventional Commits.
- **R7. Atualização upstream.** Job agendado clona as fontes no HEAD, compara com o lock e abre issue com o diff dos artefatos `supersedes` (novos, alterados, removidos). Nunca atualiza conteúdo automaticamente.
- **R8. Sem efeito colateral na instalação.** Nada de telemetria, auto-update, hook ativo por padrão ou escrita fora do diretório do plugin.

## Critérios de aceite

1. `claude plugin marketplace add <repo>` lista os 25 domínios e os profiles.
2. Instalar só `testing` não carrega descrições de nenhum outro domínio.
3. O build gera pacotes Codex, Cursor e Gemini a partir de uma skill-piloto e o eval de gatilho passa em pelo menos dois harnesses.
4. O job de atualização abre uma issue de exemplo com diff legível.

## Fora de escopo

Publicação em registries (npm, marketplaces de terceiros) — exige aprovação explícita de publicação.
