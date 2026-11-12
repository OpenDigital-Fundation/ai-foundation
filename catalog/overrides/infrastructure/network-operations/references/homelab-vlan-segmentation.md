# homelab-vlan-segmentation — reviewed procedure

Adapted by OpenDigital from `affaan-m/ECC` at `b38be6a`, `skills/homelab-vlan-segmentation/SKILL.md#how-it-works,vlan-design-template,switch-trunk-vs-access-ports,anti-patterns,best-practices`. See this domain’s PROVENANCE.yaml. This is a reviewed procedure, not an installed upstream tool or a validated runtime example.

Build a source/destination/service flow table for management, trusted clients, servers, guests and untrusted devices. Define tagged trunks, access ports, native VLAN behaviour and routing/firewall boundaries for the actual hardware. VLAN membership alone does not prove isolation.

Stage a single client and test required allowed services plus forbidden paths over IPv4/IPv6 and relevant discovery protocols. Failed ping alone is insufficient. Restrict management to an explicit admin path, not every device called trusted. Reserve DNS exceptions narrowly and confirm rule ordering. Back up and preserve console access before applying the reviewed platform-specific diff.
