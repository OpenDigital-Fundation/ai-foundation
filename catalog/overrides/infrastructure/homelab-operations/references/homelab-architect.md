# homelab-architect — reviewed procedure

Adapted by OpenDigital from `affaan-m/ECC` at `b38be6a`, `agents/homelab-architect.md#scope,workflow,safety-defaults,output-format`. See this domain’s PROVENANCE.yaml. This is a reviewed procedure, not an installed upstream tool or a validated runtime example.

Inventory gateways, switching/APs, servers/NAS, services, power, DNS/DHCP and recovery access. Match isolation, remote access and availability goals to actual hardware and operator constraints. Start with the smallest useful topology and explicit trust zones.

Keep a working internet/management path while changing one component at a time. Require backups, console access and rollback before disruptive settings. Do not expose management panels publicly or disable access controls as a shortcut. Deliver roles, topology, address/service tables, staged changes and recovery tests. General application delivery remains in platform.
