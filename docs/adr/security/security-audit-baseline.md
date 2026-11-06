# Base do domínio de segurança
- **Status:** proposto
- **Data:** 2026-11-06
- **Domínio:** security

## Contexto

Há ~32 artefatos de segurança: `security-audit` (Cloudflare, MIT, multi-fase com achados verificados e legíveis por máquina), `security-review`/`security-scan`/`security-bounty-hunter` (ECC), 12 personas do agency-agents, variantes por framework (django-, laravel-, springboot-, quarkus-, perl-security) e o Shannon (AGPL), além de checklists e políticas da SecurityStandards (NC ou sem licença).

## Decisão

`security/security-audit` (base Cloudflare) é a skill central de auditoria; variantes por framework viram `references/security.md` dos pacotes de linguagem. Skills separadas só para capacidades distintas: `threat-modeling`, `secrets-hygiene`, `agent-security` (prompt injection, ferramentas, MCP, hooks) e `supply-chain-review`. Um agent `security-auditor` executa a auditoria em contexto isolado. Shannon, checklists e políticas da SecurityStandards são referenciados em `knowledge/` por link.

## Consequências

- Um único formato de achado de segurança no catálogo inteiro.
- Pentest autônomo exige instalar o Shannon à parte, respeitando a AGPL.
