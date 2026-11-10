# `security`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

Application and agent security - audits, threat modelling, secrets, supply chain, hardening.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install security@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### knowledge

| Artefato | Estado | Quando usar |
|---|---|---|
| [`external-references`](knowledge/external-references.md) | experimental | Links and licence notes for security material referenced but not copied (Shannon, checklists, OWASP). |

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`agent-security`](skills/agent-security/SKILL.md) | experimental | Use when building, reviewing or configuring an AI agent or agent harness that reads untrusted content, calls tools, writes files, holds credentials, or loads MCP servers, hooks and plugins. Covers prompt-injection bound… |
| [`secrets-hygiene`](skills/secrets-hygiene/SKILL.md) | experimental | Use when a secret, token, key or password may have leaked (committed, logged, shipped in a bundle or image), when setting up secret scanning, or when deciding how an application should store, broker and rotate credentia… |
| [`security-audit`](skills/security-audit/SKILL.md) | experimental | Use for security questions, focused vulnerability reviews, vulnerability research, security audits or authorised pen tests of codebases, APIs, services, CLI tools, libraries and daemons. Runs the complete six-phase audi… |
| [`threat-modeling`](skills/threat-modeling/SKILL.md) | experimental | Use when designing a new system or feature that handles sensitive data, money, identity or untrusted input, before a security review, or when the user asks for a threat model. Maps data flows and trust boundaries, runs… |

## Origem e manutenção

- Entrada editorial: [manifesto de `security`](../../catalog/curation/domains/security.yaml).
- Requisitos: [spec do domínio](../../docs/specs/security/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/security/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `external-references` | contribuição original |
| `agent-security` | affaan-m/ECC, getsentry/skills, github/awesome-copilot |
| `secrets-hygiene` | getsentry/skills, github/awesome-copilot, msitarzewski/agency-agents |
| `security-audit` | SecurityStandards/skill-security-audit, affaan-m/ECC, getsentry/skills, github/awesome-copilot, msitarzewski/agency-agents |
| `threat-modeling` | getsentry/skills, msitarzewski/agency-agents, openai/skills, wshobson/agents |
