---
name: homelab-operations
description: "Use when planning or operating a home/small-lab self-hosted environment: device roles, services, storage, DNS, access, backups, recovery and staged network readiness."
license: MIT
metadata:
  domain: infrastructure
  status: experimental
---
# Homelab operations

## Establish the service and recovery goals
Inventory ISP handoff, gateway, switches/APs, hosts, storage, power, DNS/DHCP, services and remote access. Record operator skill, constraints, data value and acceptable downtime. Keep the first proposal read-only.

## Staged design
1. Assign hardware/service roles and the smallest useful topology. Separate management, trusted clients, servers, guests and untrusted devices according to actual risk and hardware capability.
2. Document addresses, reservations, service names, storage ownership, credentials and external dependencies. Avoid overlapping VPN/site ranges and unmanaged duplicate DHCP services.
3. Before changing DNS, VLANs or VPN routes, establish stable infrastructure addresses, a tested fallback and console access. Keep the operator's recovery path working throughout.
4. Design backups from recovery goals, with independent copies and a demonstrated restore test. A running backup job is not evidence that data can be restored.
5. Plan service installation/update as reviewed, versioned changes. No remote-shell installer, public management interface, automatic key rotation or wholesale firewall replacement by default.
6. Move one test client/service at a time; verify connectivity, access isolation, name resolution and rollback before wider rollout. Record final inventory and unresolved risks.

## Deliverable
Topology, service/address table, storage/backup plan, phased changes, verification and recovery runbook. Use infrastructure:network-operations for packet-path diagnosis and platform:deployment for application delivery. Do not promise enterprise availability from a home deployment.

## References

Load only what the task needs:

- [`references/homelab-architect.md`](references/homelab-architect.md) — Reviewed adaptation: homelab-architect; version and approval assumptions are explicit.
- [`references/homelab-network-readiness.md`](references/homelab-network-readiness.md) — Reviewed adaptation: homelab-network-readiness; version and approval assumptions are explicit.
- [`references/homelab-network-setup.md`](references/homelab-network-setup.md) — Reviewed adaptation: homelab-network-setup; version and approval assumptions are explicit.
