# homelab-network-readiness — reviewed procedure

Adapted by OpenDigital from `affaan-m/ECC` at `b38be6a`, `skills/homelab-network-readiness/SKILL.md#safety-rules,required-inventory,change-sequence,review-checklist,anti-patterns`. See this domain’s PROVENANCE.yaml. This is a reviewed procedure, not an installed upstream tool or a validated runtime example.

Before DNS, VLAN, firewall or VPN changes, capture the existing topology, platform/firmware, uplinks/trunks, addressing, DHCP/resolvers, expected flows and management path. Confirm console or out-of-band recovery and a local backup of relevant settings.

Create a new zone without moving critical devices, test one client, verify address/route/DNS and both allow/deny flows, then migrate a low-risk group. Preserve recovery at each stage. Do not change the whole network from a remote-only session or use an allow-all rule as a temporary shortcut. A plan is not authorization to apply it.
