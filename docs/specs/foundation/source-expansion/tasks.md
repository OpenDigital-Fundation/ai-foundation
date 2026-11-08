# Tarefas — Expansão de fontes

- [x] **T0.** Detecção de licença por pasta no inventário (pré-requisito para fontes com licença por skill).
- [x] **T1.** Fatia 1: oficiais e empresas. 240 itens decididos em `catalog/curation/exclusions.yaml` (144 Trail of Bits e 1 Sentry por licença CC BY-SA, ligados em `security/external-references`; Figma por termos próprios; integrações de fornecedor; manutenção interna). Nenhum conteúdo copiado nesta fatia.
  - [ ] **T1.1.** Fundir o conteúdo útil dos itens marcados `duplicate-of`, por receita no manifesto do domínio dono, e mover a chave para `supersedes`. Prioridade: `openai/skills` `security-threat-model` → `security/threat-modeling`; `getsentry/skills` `gha-security-review` e `django-access-review` → `security/security-audit`, `skill-scanner` → `security/agent-security`, `secret-serialization` → `security/secrets-hygiene`, `iterate-pr` → `platform/github-operations`, `prompt-optimizer` → `ai-engineering/prompt-engineering`.
- [ ] **T2.** Fatia 2: `github/awesome-copilot`.
- [ ] **T3.** Fatia 3: grandes coleções.
- [ ] **T4.** Fatia 4: ciência.
