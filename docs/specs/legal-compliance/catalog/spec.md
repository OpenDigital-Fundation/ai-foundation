# Spec — Catálogo do domínio `legal-compliance`

- **Domínio:** legal-compliance
- **Status:** em implementação (Onda 3)
- **Fronteira:** contratos, conformidade regulatória, privacidade jurídica.

## Resultado (gerado por `tools.curation.bundle` a partir de [`bundles/business.yaml`](../../../../catalog/decisions/bundles/business.yaml))

| Artefato | Base | Referências |
|---|---|---|
| `compliance-programs` | `security-compliance-auditor` | `data-privacy-officer`, `legal-compliance-checker` |
| `contracts` | `master-agreement-generator` | `legal-document-review`, `legal-client-intake` |

## Notas

- Base em personas do agency-agents: o texto é persona, não procedimento verificável. Revisar cada skill e reescrever o corpo como passos com critério de saída antes de promover a `stable`.
- Saídas jurídicas são rascunhos para revisão por profissional habilitado; as descrições dizem isso.
