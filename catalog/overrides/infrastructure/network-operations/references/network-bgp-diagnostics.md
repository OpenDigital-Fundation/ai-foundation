# network-bgp-diagnostics — reviewed procedure

Adapted by OpenDigital from `affaan-m/ECC` at `b38be6a`, `skills/network-bgp-diagnostics/SKILL.md#read-only-triage-flow,state-interpretation,route-policy-checks,change-window-only,anti-patterns`. See this domain’s PROVENANCE.yaml. This is a reviewed procedure, not an installed upstream tool or a validated runtime example.

Record neighbor, address family, VRF, ASNs, session state and last reset reason. Establish peer-source reachability and transport, then review negotiated families, route policy, accepted paths and installed forwarding state. Use the target platform's read-only equivalents.

Compare advertisements, received routes and selected routes where supported; an established session does not prove useful forwarding. Preserve timestamps and sensitive configuration safely. Peer resets, policy changes, counter clearing and route withdrawals belong to a separate change window with explicit approval and rollback.
