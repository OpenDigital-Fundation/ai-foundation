---
name: supply-chain-planning
description: "Use when planning physical supply chains: demand/capacity, inventory policy, suppliers, lead-time risk, sourcing alternatives and scenario-based total cost."
license: MIT
metadata:
  domain: logistics
  status: experimental
---
# Supply-chain planning

## Bound the physical system
Record products/SKUs, locations, units, demand history, lead-time distributions, service definition, capacity, shelf-life/safety constraints and applicable contracts. Do not confuse physical supply chains with software dependency security.

## Plan with explicit assumptions
1. Reconcile demand, receipts, stock, backorders, costs and units over the same period. Quantify missingness and distinguish orders, shipments and consumption.
2. Identify bottlenecks, supplier concentration, substitution constraints and correlated failure modes. Record qualification time/cost and capacity, not just supplier count.
3. Choose a replenishment model that matches demand/lead-time behaviour and constraints. EOQ or a normal-demand safety-stock formula is conditional on its assumptions, not a universal recommendation.
4. Compare scenarios using total landed/lifecycle cost, working capital, service and risk. Define time units and cost basis before computing; test sensitivity to seasonality, disruption and intermittent demand.
5. Check proposals against MOQ, packaging multiples, capacity, cash, shelf life and recovery options. Supplier awards, hedges, purchases or contractual commitments need responsible approval.
6. Backtest the policy and report service/cost tradeoffs, assumptions and an owner-controlled review cadence.

## Deliverable
A reconciled baseline, assumptions/units register, scenarios, feasible policy, risk/contingency plan and measurable review criteria. Financial accounting belongs to finance; generic project execution to operations; dispatch and exceptions to logistics:logistics-operations.

## References

Load only what the task needs:

- [`references/supply-chain-strategist.md`](references/supply-chain-strategist.md) — Reviewed adaptation: Supply Chain Strategist; version and approval assumptions are explicit.
