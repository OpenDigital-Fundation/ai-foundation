# homelab-pihole-dns — reviewed procedure

Adapted by OpenDigital from `affaan-m/ECC` at `b38be6a`, `skills/homelab-pihole-dns/SKILL.md#how-pi-hole-works,troubleshooting,anti-patterns,best-practices`. See this domain’s PROVENANCE.yaml. This is a reviewed procedure, not an installed upstream tool or a validated runtime example.

Treat a local DNS filter as a resolver policy component, not proof that every advertisement, tracker or encrypted application lookup is blocked. Record resolver address, upstreams, client distribution and failure/recovery paths; a second equivalent resolver can support policy-preserving redundancy.

Diagnose with authorized read-only status/logs and a bounded query to the intended resolver. Review logs as sensitive data. Allow-list changes, blocklist refreshes, DHCP changes, restarts and installation are separate approved operations using the installed version's documented interface. Use home.arpa for home naming rather than inheriting conflicting home.lan examples. No remote-shell installer is included.
