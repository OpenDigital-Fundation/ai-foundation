---
name: defi-engineering
description: "Use when engineering or reviewing DeFi mechanism invariants, AMM/share accounting, token decimals, oracle assumptions, collateral/liquidation flows or protocol simulations."
license: MIT
metadata:
  domain: web3
  status: experimental
---
# DeFi engineering

## Model value and trust
Define assets by chain ID and contract address, units/decimals, balances versus internal accounting, actors, privileges, oracle sources, timing and failure assumptions. This is protocol engineering, not a recommendation to buy, lend or trade.

## Mechanism workflow
1. Draw deposits, shares, swaps, debt, fees, collateral and withdrawals as balance-sheet transitions. State conservation, solvency and access-control invariants appropriate to the mechanism.
2. Verify token metadata and non-standard behaviours. Use exact integer/decimal arithmetic with explicit rounding direction; do not assume every token has 18 decimals or returns successful metadata calls.
3. Evaluate donation/inflation, reentrancy, fee-on-transfer, rebasing, unusual decimals, zero liquidity, stale/manipulated oracles and governance concentration against the model.
4. Simulate ordinary, boundary and adversarial sequences locally. Record parameters and sensitivities; illustrative rates and liquidity are not forecasts or validated production defaults.
5. Implement protocol-specific slippage, deadlines, oracle freshness and emergency controls where required, and test their failure modes. A checklist does not prove economic safety.
6. Hand independent security review a reproducible model, invariants, tests, privileged actions and unresolved assumptions before any real-asset deployment.

## Handoff
A unit-checked mechanism specification, adversarial scenarios, simulation/test evidence and change/approval boundaries. No wallet signing, real-money transaction or paid RPC use without explicit authorization. Generic audits, secrets and operational incidents stay in security/platform.

## References

Load only what the task needs:

- [`references/defi-amm-security.md`](references/defi-amm-security.md) — Reviewed adaptation: defi-amm-security; version and approval assumptions are explicit.
- [`references/evm-token-decimals.md`](references/evm-token-decimals.md) — Reviewed adaptation: evm-token-decimals; version and approval assumptions are explicit.
