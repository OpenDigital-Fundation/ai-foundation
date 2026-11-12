# `infrastructure`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

Networks and self-hosted labs - connectivity, routing, DNS, VPN, segmentation, local services, storage and recovery; application delivery stays in platform.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install infrastructure@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`homelab-operations`](skills/homelab-operations/SKILL.md) | experimental | Use when planning or operating a home/small-lab self-hosted environment: device roles, services, storage, DNS, access, backups, recovery and staged network readiness. |
| [`network-operations`](skills/network-operations/SKILL.md) | experimental | Use when diagnosing or reviewing an authorized network: topology, interfaces, routing/BGP, segmentation, DNS, DHCP, firewall paths or VPN connectivity. |

## Origem e manutenção

- Entrada editorial: [manifesto de `infrastructure`](../../catalog/curation/domains/infrastructure.yaml).
- Requisitos: [spec do domínio](../../docs/specs/infrastructure/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/infrastructure/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `homelab-operations` | affaan-m/ECC |
| `network-operations` | affaan-m/ECC |
