---
name: network-operations
description: "Use when diagnosing or reviewing an authorized network: topology, interfaces, routing/BGP, segmentation, DNS, DHCP, firewall paths or VPN connectivity."
license: MIT
metadata:
  domain: infrastructure
  status: experimental
---
# Network operations

## Inventory before commands
Identify owner, authorized targets, exact platform/version, topology, addressing, routing domains, expected flows, current symptoms and the last known good state. Start with read-only evidence; broad scanning is not implicit authorization.

## Diagnose by boundary
1. Check physical/link state and counter deltas, then addressing/neighbor resolution, routes, DNS and policy. Compare an affected path with a known working path.
2. Correlate observations with timestamps and a bounded collection window. Counter totals without interval, link rate and resets are not error rates.
3. For BGP, distinguish neighbor transport/session state, address family, route policy, accepted paths and installed forwarding state. Do not reset peers or clear counters during read-only triage.
4. For VLAN/firewall design, specify required source/destination/service flows and test both expected allow and deny behaviour, including IPv6 and management access. Failed ping alone does not establish isolation.
5. For DNS/VPN, separate resolver reachability, application bypasses, peer handshakes, routes and forwarding policy. Keep keys, logs and full configurations out of public outputs.
6. Propose the smallest reversible change with exact platform syntax, backup, maintenance window, console/out-of-band path and validation. Apply only after specific authorization.

## Handoff
Evidence, ranked hypotheses, bounded tests, proposed diff, risks, rollback and success criteria. Do not disable authentication/firewalls as a shortcut. Homelab planning belongs to infrastructure:homelab-operations; application deployment/SRE stays in platform.

## References

Load only what the task needs:

- [`references/homelab-pihole-dns.md`](references/homelab-pihole-dns.md) — Reviewed adaptation: homelab-pihole-dns; version and approval assumptions are explicit.
- [`references/homelab-vlan-segmentation.md`](references/homelab-vlan-segmentation.md) — Reviewed adaptation: homelab-vlan-segmentation; version and approval assumptions are explicit.
- [`references/homelab-wireguard-vpn.md`](references/homelab-wireguard-vpn.md) — Reviewed adaptation: homelab-wireguard-vpn; version and approval assumptions are explicit.
- [`references/network-bgp-diagnostics.md`](references/network-bgp-diagnostics.md) — Reviewed adaptation: network-bgp-diagnostics; version and approval assumptions are explicit.
- [`references/network-config-validation.md`](references/network-config-validation.md) — Reviewed adaptation: network-config-validation; version and approval assumptions are explicit.
- [`references/network-interface-health.md`](references/network-interface-health.md) — Reviewed adaptation: network-interface-health; version and approval assumptions are explicit.
