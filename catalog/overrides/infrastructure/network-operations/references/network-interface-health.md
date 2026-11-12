# network-interface-health — reviewed procedure

Adapted by OpenDigital from `affaan-m/ECC` at `b38be6a`, `skills/network-interface-health/SKILL.md#counter-reference,diagnosis-flow,anti-patterns`. See this domain’s PROVENANCE.yaml. This is a reviewed procedure, not an installed upstream tool or a validated runtime example.

Capture interface state, negotiated speed/duplex, MTU, recent resets and error/drop counter deltas over a stated interval. Relate counts to traffic volume and compare both ends and a working path. A cumulative counter alone is not an error rate or root cause.

Separate physical integrity, congestion, policy drops and host/application symptoms. Gather bounded evidence before proposing cable, transceiver or configuration changes. Do not clear counters, bounce interfaces or alter link negotiation during read-only diagnosis. Record competing hypotheses and the next discriminating test.
