# Skills encontradas na máquina do mantenedor (2026-11-06)

Levantamento das skills, agents e extensões instaladas localmente, para garantir que nenhuma referência útil ficasse de fora do catálogo. Caminhos pessoais omitidos.

| Onde | Skill / extensão | Origem | Decisão |
|---|---|---|---|
| Claude Code (pessoal) | `handoff` | criada pelo mantenedor | base de `workflow:handoff` (contribuição) |
| Claude Code (pessoal) | `migrar-app-portais` | criada pelo mantenedor | pasta vazia; nada a importar |
| Claude Code / Agent Skills | `orca-cli`, `orchestration` | `stablyai/orca` (instalador) | ferramenta do Orca; fora do catálogo |
| Claude Code / Agent Skills | `find-skills` | `vercel-labs/skills` (instalador) | coberto por `agent-engineering:skill-authoring` (busca antes de criar) |
| Claude Code / Agent Skills | `reverse-engineer-anything` | `SecurityStandards/agent-reverse-engineer` | já registrado como fonte de referência |
| claude.ai (sincronizadas) | `docx`, `pdf`, `pptx`, `xlsx`, `skill-creator`, `mcp-builder`... | nativas da Anthropic | já cobertas por `anthropics/skills` |
| Codex | `superpower` | criada pelo mantenedor | referência em `workflow:brainstorming` (contribuição) |
| Codex | `ui-ux-pro-max` | `nextlevelbuilder/ui-ux-pro-max-skill` | já é fonte |
| Codex | `react-best-practices`, `web-design-guidelines` | `vercel-labs/agent-skills` | nova fonte: React em `languages:typescript`; guidelines só referência (sem licença declarada) |
| Codex | `playwright-best-practices` | `currents-dev/playwright-best-practices-skill` | nova fonte: `testing:browser-testing` |
| Codex | `codex-primary-runtime` | — | pasta vazia |
| Gemini CLI | `superpowers` | `obra/superpowers` | já é fonte |
| Gemini CLI | `accessibility-agents` | `Community-Access/accessibility-agents` | nova fonte: domínio `accessibility` reconstruído |
| Gemini CLI | `godoctor` | `danicat/godoctor` | referência em `languages/external-tools` |
| Gemini CLI | `frontend-design` | `ankitchiplunkar/frontend-design` | excluída: persona genérica, mais fraca que `ui:visual-design` |
| Projeto de cliente | `issue-routing-triage` | criada pelo mantenedor | generalizada em `workflow:issue-triage` (sem dados do cliente) |
| Projeto de cliente | `stacked-pull-requests` | criada pelo mantenedor | generalizada em `platform:git-workflow` |
| Projeto de cliente | `revisor-de-codigo` | mantenedor e Danilo Ribeiro | traduzida e generalizada: base de `code-quality:codebase-audit` |
| Projeto de cliente | `react-doctor` | `millionco/react-doctor` | só referência: licença proíbe uso em avaliação de IA |
| Projeto REA | `rea-changelog-update`, `rea-ci-tests-audit`, `rea-tool-design` | outros autores do projeto REA | internas daquele projeto; fora |
