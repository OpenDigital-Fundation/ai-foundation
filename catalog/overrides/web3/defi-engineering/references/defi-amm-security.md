# defi-amm-security — reviewed procedure

Adapted by OpenDigital from `affaan-m/ECC` at `b38be6a`, `skills/defi-amm-security/SKILL.md#execution-safety,security-checklist`. See this domain’s PROVENANCE.yaml. This is a reviewed procedure, not an installed upstream tool or a validated runtime example.

Review the mechanism's accounting and trust model before applying a checklist. Evaluate external-call/reentrancy boundaries, share inflation/donations, fee-on-transfer/rebasing behaviour, oracle manipulation/freshness, rounding, slippage, deadlines and privileged controls as applicable to the actual protocol.

Model adversarial sequences and state invariants; measure received tokens where the mechanism requires it and test zero/low liquidity and failure states. Static analysis and fuzzing support review but are not an economic-safety certificate. Use local/disposable environments, never secrets or real signing credentials; paid RPC/tool installs and production actions require explicit authorization.
