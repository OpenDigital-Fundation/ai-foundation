---
name: smart-contract-development
description: "Use when designing, implementing and testing blockchain smart contracts, token interfaces, upgrade/storage layouts or a deployment plan, excluding investment recommendations and live value transfers."
license: MIT
metadata:
  domain: web3
  status: experimental
---
# Smart contract development

## Establish the contract system
Record chain/network, compiler and toolchain versions, dependencies, token standards, trust assumptions, privileged roles, upgrade model and asset flows. Do not request seed phrases or signing keys.

## Build and verify
1. Express state transitions, authorization rules, accounting units, events and invariants before code. Decide immutable versus upgradeable design from requirements, not a default template.
2. Select maintained libraries compatible with the pinned compiler. Review initialization, storage layout, external-call boundaries, reentrancy and failure behaviour; library use is not an audit certificate.
3. Test intended and unauthorized transitions, malformed inputs, edge amounts, rounding, events and role changes. Implement fixtures against the actual contract interface, not an undefined sample Token contract.
4. Add fuzz/invariant tests and upgrade-state preservation tests where applicable. Use disposable local chains; any external RPC or fork requires an authorized endpoint and a pinned block with no signing capability.
5. Measure gas with a representative versioned build; do not treat a universal coverage percentage or gas threshold as proof of security.
6. Prepare a deployment/verification plan with constructor/proxy parameters, roles, pause/recovery and rollback limits. Production or testnet transactions, ownership transfers and publication require separate authorization.

## Deliverable
Code or design, invariant/test evidence, dependency versions, known limitations and the reviewed deployment plan. Security auditing belongs to security:security-audit; protocol accounting and mechanisms to web3:defi-engineering. No profitability promise or investment advice is part of this skill.

## References

Load only what the task needs:

- [`references/solidity-smart-contract-engineer.md`](references/solidity-smart-contract-engineer.md) — Reviewed adaptation: Solidity Smart Contract Engineer; version and approval assumptions are explicit.
- [`references/web3-testing.md`](references/web3-testing.md) — Reviewed adaptation: web3-testing; version and approval assumptions are explicit.
- [`references/nft-standards.md`](references/nft-standards.md) — Reviewed adaptation: nft-standards; version and approval assumptions are explicit.
