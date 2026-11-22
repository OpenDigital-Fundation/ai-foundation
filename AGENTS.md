# AGENTS.md — OpenDigital AI Foundation

Fonte canônica de verdade para agentes e pessoas que trabalham neste repositório.

## O que é

Coletânea curada de **skills, agents, hooks, rules e configurações MCP** para agentes de IA de código (Claude Code, Codex, Cursor, Gemini CLI, OpenCode e outros). A coletânea é **deduplicada por domínio**: cada capacidade existe uma única vez, no domínio dono dela. Exemplo: não existe "ui-ux-pro-max"; existe uma skill de UI no domínio `ui` e uma de UX no domínio `ux`.

## Layout

```
domains/<domínio>/                 # cada domínio é um plugin instalável
  .claude-plugin/plugin.json
  skills/<skill>/SKILL.md          # capacidades reutilizáveis (+ references/ scripts/ assets/ evals/)
  agents/<agent>.md                # agentes especializados (contexto isolado)
  workflows/<workflow>/SKILL.md    # orquestrações de skills/agents com portões (carregadas como skill)
  prompts/<prompt>.md              # prompts compartilhados que não disparam sozinhos
  rules/<rule>.md                  # padrões e instruções sempre ativos
  hooks/                           # guardrails determinísticos, opt-in
  mcps/<server>.json               # configurações MCP com versão fixada
  templates/                       # modelos (spec, ADR, AGENTS.md, PR...)
  knowledge/                       # referência estática citável
  evals/                           # testes e avaliações do domínio
  PROVENANCE.yaml                  # origem de cada artefato
profiles/<perfil>.yaml             # bundles entre domínios (ex.: fullstack-web)
evals/routing/                     # evals de roteamento: o prompt certo dispara a skill certa
catalog/
  curation/domains/<domínio>.yaml   # fonte editorial: registros, receitas e importações
  curation/exclusions.yaml         # decisões editoriais de exclusão
  inventory/                       # levantamento upstream e hashes de conteúdo restrito
  overrides/                       # ajustes locais reaplicados na geração
  catalog.yaml                     # projeção gerada: domínio × capacidade → artefato
  sources.lock.yaml                # fontes upstream com commit fixado
  exclusions.yaml                  # projeção gerada das exclusões
docs/
  architecture/                    # contrato de manutenção atual
  reviews/                         # revisões com baseline e evidências
  <domínio>/specs/ROADMAP.md       # ordem e dependências das specs do domínio
  <domínio>/specs/<feature>/       # spec.md, plan.md, tasks.md
  <domínio>/adr/AAAA-MM-DD-<decisão>.md  # um ADR por decisão (Nygard)
  transversal/{specs,adr}/         # o que atravessa domínios, mesma estrutura
  specs/<domínio>/<feature>/       # legado (transição): aceito, não criar novos
  adr/<domínio>/<decisão>.md       # legado (transição): aceito, não criar novos
tools/                             # validadores e geradores (CI)
```

## Convenções

- **Specs e ADRs sem numeral**, organizados por domínio: `docs/<domínio>/specs/<feature>/{spec,plan,tasks}.md` e `docs/<domínio>/adr/AAAA-MM-DD-<decisão>.md`. O que atravessa domínios vai em `docs/transversal/`. `<domínio>` é um domínio de `catalog/domains.yaml`, `foundation` ou `transversal`. A ordem de execução fica em `docs/<domínio>/specs/ROADMAP.md`; o status fica no cabeçalho do ADR e a data também vai no nome do arquivo.
- **Transição:** specs e ADRs existentes ficam em `docs/specs/<domínio>/<feature>/` e `docs/adr/<domínio>/<slug>.md`; não mover nem renomear. O validador aceita os dois caminhos e recusa a mesma feature nos dois. Documento novo usa só o layout novo. A migração em lote tem issue própria. Decisão: `docs/foundation/adr/2026-11-21-docs-layout-domain-first.md`.
- **Uma spec = um domínio ou uma feature**, com exatamente um `plan.md` e um `tasks.md`.
- **Governança em pt-BR; artefatos em inglês** (ver `docs/adr/foundation/english-artifacts-portuguese-governance.md`).
- **Nomes sem marca**: nada de `pro-max`, `superpowers`, `ponytail`, `ecc` nos nomes publicados. A origem vai para `PROVENANCE.yaml`.
- **Fonte editorial:** metadados e receitas em `catalog/curation/domains/<domínio>.yaml`; registro e exclusões públicos são gerados. Não editar projeções diretamente.
- **Referências:** `SKILL.md` somente na entrada pública de skills/workflows; guias em `references/` usam `README.md`, fontes tipográficas em `assets/fonts/`. Agentes privados de uma skill não são agentes públicos do domínio.
- **Antes de criar um artefato**, consultar `catalog/catalog.yaml`. Se a capacidade já existe, melhorar o existente; nunca criar um paralelo.

## Regras de contribuição

1. Todo artefato novo ou fundido passa pela spec do seu domínio.
2. Só se copia conteúdo com licença permissiva (MIT, Apache-2.0, BSD). AGPL, não comercial (CC BY-NC) e proprietário só podem ser referenciados.
3. Toda cópia ou fusão registra fonte, commit, licença e modificações em `PROVENANCE.yaml`.
4. Uma skill só sai de `experimental` para `stable` com evals de gatilho e de tarefa passando.
5. Commits assinados (GPG), Conventional Commits; nada vai para `main` sem PR.

## Comandos

```sh
uv run pytest -q
uv run python -m tools.validate
uv run python -m tools.catalog rebuild
uv run python -m tools.build
uv run python -m tools.build docs
```

Curadoria por domínio: `uv run python -m tools.curation <sources-dir> --domain <domínio>`. Recria conteúdo gerado: conferir mudanças locais antes de executar. Adaptadores: `uv run python -m tools.build adapters` (saída local em `dist/`). Avaliações com modelo são separadas e podem gerar custo.

Contrato de edição e reconstrução: [docs/architecture/repository-layout.md](docs/architecture/repository-layout.md). Não publicar nem remover worktrees sem a aprovação aplicável.
