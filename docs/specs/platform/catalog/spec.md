# Spec — Catálogo do domínio `platform`

- **Domínio:** platform
- **Status:** em implementação (Onda 2)
- **Fronteira:** Git/GitHub, CI/CD, containers, deploy, observabilidade, SRE, incidentes.

## Resultado (gerado por `tools.curation.bundle` a partir de [manifesto editorial](../../../../catalog/curation/domains/platform.yaml))

| Artefato | Base | Referências |
|---|---|---|
| `git-workflow` | procedimento original (curto; operações destrutivas exigem aprovação) | ECC `git-workflow`, agency *Git Workflow Master*, mattpocock `setup-pre-commit`; absorve ECC `conventional-commit-review` |
| `github-operations` | ECC `github-ops` (sem o checklist de release interno do ECC) | — |
| `deployment` | ECC `deployment-patterns` | ECC `docker-patterns`, `kubernetes-patterns`, `canary-watch`, comando `pm2`; agency *DevOps Automator*, *Platform Engineer*, *Mobile Release Engineer* |
| `reliability` | agency *SRE* | ECC `dashboard-builder`; agency *Infrastructure Maintainer* |
| `incident-response` | agency *Incident Response Commander* | agency *Incident Responder* (incidentes de segurança) |

`testing:browser-testing` (base Anthropic `webapp-testing`, Apache-2.0 com aviso) foi gerado no mesmo bundle; ver a spec de `testing`.

## Pendências

- Guardrails de agente (mattpocock `git-guardrails-claude-code`, ECC `safety-guard`, `gateguard`) → `agent-engineering`.
- ECC `terminal-ops`, `terminal-opener`: decidir.
