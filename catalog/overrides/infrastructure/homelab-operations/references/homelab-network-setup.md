# homelab-network-setup — reviewed procedure

Adapted by OpenDigital from `affaan-m/ECC` at `b38be6a`, `skills/homelab-network-setup/SKILL.md#ip-plan,dhcp-and-dns,cabling-and-wi-fi,anti-patterns`. See this domain’s PROVENANCE.yaml. This is a reviewed procedure, not an installed upstream tool or a validated runtime example.

Design addresses from actual device counts, segmentation and expected VPN/site overlap; private example ranges are not prescribed defaults. Assign stable reservations to infrastructure and document gateway, DHCP scope and resolver ownership. Avoid duplicate unmanaged DHCP and unexplained double NAT.

Use an appropriate local naming namespace; [RFC 8375 reserves home.arpa](https://www.rfc-editor.org/rfc/rfc8375.html) for home-network naming. Record port/SSID mappings, wired/mesh backhaul and power dependencies. Verify one client and recovery before changing shared DNS/DHCP. DNS filtering, backups and service availability need their own tests rather than assumptions from a topology diagram.
