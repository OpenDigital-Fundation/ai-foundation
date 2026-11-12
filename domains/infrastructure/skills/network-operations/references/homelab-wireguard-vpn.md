# homelab-wireguard-vpn — reviewed procedure

Adapted by OpenDigital from `affaan-m/ECC` at `b38be6a`, `skills/homelab-wireguard-vpn/SKILL.md#how-wireguard-works,split-tunnel-vs-full-tunnel,troubleshooting,anti-patterns,best-practices`. See this domain’s PROVENANCE.yaml. This is a reviewed procedure, not an installed upstream tool or a validated runtime example.

Identify peer keys, endpoint reachability, intended routes, resolver behaviour and forwarding/firewall policy. Keep private keys out of prompts and logs; distinct peer identity supports revocation and accountability. Choose split/full tunnel from requirements, not as a universal default.

Diagnose handshake, routing and authorized read-only interface status separately. NAT traversal/keepalive, IPv6 and overlapping subnets depend on the environment. Avoid blanket forwarding acceptance. Restarts, route changes, public port exposure and key rotation require a reviewed change and recovery path. Do not copy a fixed keepalive or full-LAN AllowedIPs list without checking the actual need.
