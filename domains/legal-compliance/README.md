# `legal-compliance`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

Contracts, regulatory compliance, legal privacy.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install legal-compliance@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`compliance-programs`](skills/compliance-programs/SKILL.md) | experimental | Use when preparing for or checking compliance: SOC 2, ISO 27001, GDPR, CCPA, HIPAA or PCI-DSS readiness, privacy programmes and data processing, control mapping, evidence collection and policy gaps. Not legal advice. |
| [`contracts`](skills/contracts/SKILL.md) | experimental | Use when drafting, reviewing or organising contracts: master service agreements and order forms, clause review against a playbook, redlines, client intake and matter organisation. Drafts are for review by a qualified la… |

## Origem e manutenção

- Entrada editorial: [manifesto de `legal-compliance`](../../catalog/curation/domains/legal-compliance.yaml).
- Requisitos: [spec do domínio](../../docs/specs/legal-compliance/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/legal-compliance/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `compliance-programs` | github/awesome-copilot, msitarzewski/agency-agents, wshobson/agents |
| `contracts` | affaan-m/ECC, msitarzewski/agency-agents |
