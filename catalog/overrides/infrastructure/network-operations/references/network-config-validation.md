# network-config-validation — reviewed procedure

Adapted by OpenDigital from `affaan-m/ECC` at `b38be6a`, `skills/network-config-validation/SKILL.md#dangerous-command-detection,duplicate-ips-and-subnet-overlaps,management-plane-checks,security-hygiene-checks,anti-patterns`. See this domain’s PROVENANCE.yaml. This is a reviewed procedure, not an installed upstream tool or a validated runtime example.

Review an explicit configuration diff against intended topology and access policy. Check address/subnet overlaps, management reachability, authentication, secrets, interface membership, routing and the effects of default policies and rule ordering.

Flag high-impact operations such as flushing rules or disabling protections, but do not treat a regex/pattern match as a complete vendor parser or proof of safety. Use the actual platform's validation/dry-run capability when available and authorized. Preserve known-good settings and console recovery; a reviewed config is still not permission to apply it.
