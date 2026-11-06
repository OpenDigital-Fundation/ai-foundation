# Tarefas — Governança do catálogo

- [x] **T1.** Criar `catalog/schema/catalog.schema.json`, `exclusions.schema.json` e `skill-frontmatter.schema.json`. Verificar: exemplos do `plan.md` validam; um exemplo com `type: command` falha.
- [x] **T2.** Criar `catalog/naming.yaml` com termos proibidos (`pro`, `max`, `ultimate`, `v2`, `superpowers`, `ponytail`, `ecc`, `matt`, `hallmark`, `karpathy`, `claude-code` como sufixo). Verificar: `ui-ux-pro-max` é rejeitado e `visual-design` passa.
- [x] **T3.** Criar `domains/<domínio>/.claude-plugin/plugin.json` para os 25 domínios de R1, com `name`, `description` (a frase de fronteira) e `version: 0.0.0`. Verificar: `claude plugin validate` (ou equivalente) passa para cada um.
- [x] **T4.** Criar `catalog/catalog.yaml` e `catalog/exclusions.yaml` vazios e válidos.
- [x] **T5.** Documentar no `AGENTS.md` o fluxo "consultar catálogo antes de criar artefato". Verificar: revisão humana.
- [ ] **T6.** Revisão: aprovar a tabela de domínios de R1 (é a decisão mais difícil de reverter depois).
