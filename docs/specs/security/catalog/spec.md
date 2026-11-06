# Spec — Catálogo do domínio `security`

- **Domínio:** security
- **Status:** em implementação (Onda 1)
- **ADR:** [security-audit-baseline](../../../adr/security/security-audit-baseline.md)
- **Fronteira:** segurança de aplicação e de agente — auditoria, threat modeling, segredos, supply chain, hardening.

## Resultado

| Artefato | Tipo | Base | Fundidos |
|---|---|---|---|
| `security-audit` | skill | Cloudflare via `SecurityStandards/skill-security-audit` (intacta: modos orientação/auditoria completa, sandbox obrigatório, validadores de achados) | ECC `security-review`, `security-bounty-hunter`, agent `security-reviewer`, rule `security`; agency *Application Security Engineer*, *AI-Generated Code Security Auditor*, *Penetration Tester* |
| `threat-modeling` | skill | persona *Security Architect* (agency) reescrita como procedimento | — |
| `secrets-hygiene` | skill | persona *Secrets & Credential Hygiene Engineer* (agency) reescrita | — |
| `agent-security` | skill | ECC `agent-security-hardening` | ECC `mcp-dependency-review` (referência), `security-scan` |
| `external-references` | knowledge | original | links para Shannon (AGPL), checklists (CC BY-NC-SA), `security-standards` (sem licença), OWASP |

Variantes por framework (`django-`, `laravel-`, `springboot-`, `quarkus-security`) vão para `languages/<x>/references/security.md`.

## Decisões de conteúdo

- Nenhum agent de segurança próprio: o `security-audit` já define papéis delegados (`research`, `general`) neutros quanto ao harness.
- No runbook de vazamento, reescrever o histórico do git exige aprovação explícita do usuário (operação destrutiva).

## Pendências de verificação

- Os testes Node que vêm com o `security-audit` (`validate-findings.test.cjs`, `validate-coverage-ledger.test.cjs`) ainda não rodaram aqui: executar código do upstream precisa de aprovação.

## Próximos artefatos (ainda não implementados)

- `supply-chain-review`: avaliar contra `SUPPLY-CHAIN-AND-RELEASE.md` do `security-audit` antes de criar.
- Personas *Cloud Security Architect*, *Identity & Access Engineer*, *Privacy Engineer*: decidir entre referências do `security-audit` e skills próprias.
- *Compliance Auditor*, *Data Privacy Officer* → `legal-compliance`; *Incident Responder* → `platform`; *Threat Detection* e *Threat Intelligence* → fora de escopo v1.
