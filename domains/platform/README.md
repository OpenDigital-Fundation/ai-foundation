# `platform`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

Git and GitHub, CI/CD, containers, deployment, observability, SRE, incidents.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install platform@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`deployment`](skills/deployment/SKILL.md) | experimental | Use when containerising, deploying or releasing software: Dockerfiles and Compose, Kubernetes workloads, CI/CD pipelines, health checks, blue-green and canary rollouts, rollback, post-deploy verification, process manage… |
| [`git-workflow`](skills/git-workflow/SKILL.md) | experimental | Use when choosing a branching strategy, writing commit messages, tidying history before a merge, resolving conflicts, rebasing versus merging, or setting up pre-commit hooks with formatting, type checks and tests. |
| [`github-operations`](skills/github-operations/SKILL.md) | experimental | Use when operating a GitHub repository with the gh CLI: managing pull requests and issues, checking and re-running CI, configuring Actions, branch protection and releases, or monitoring Dependabot and security alerts. |
| [`incident-response`](skills/incident-response/SKILL.md) | experimental | Use when production is down or degraded, an alert fires, a breach is suspected, or a postmortem is due: assess severity, coordinate responders, communicate status, contain, recover, preserve evidence and write a blamele… |
| [`reliability`](skills/reliability/SKILL.md) | experimental | Use when defining SLOs and error budgets, adding logs, metrics and traces, building operator dashboards (Grafana, SigNoz), planning capacity, running chaos experiments, or maintaining infrastructure health. |

## Origem e manutenção

- Entrada editorial: [manifesto de `platform`](../../catalog/curation/domains/platform.yaml).
- Requisitos: [spec do domínio](../../docs/specs/platform/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/platform/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `deployment` | affaan-m/ECC, github/awesome-copilot, mattpocock/skills, msitarzewski/agency-agents, wshobson/agents |
| `git-workflow` | affaan-m/ECC, github/awesome-copilot, mattpocock/skills, msitarzewski/agency-agents |
| `github-operations` | affaan-m/ECC, getsentry/skills, github/awesome-copilot |
| `incident-response` | github/awesome-copilot, msitarzewski/agency-agents, wshobson/agents |
| `reliability` | affaan-m/ECC, github/awesome-copilot, msitarzewski/agency-agents, wshobson/agents |
