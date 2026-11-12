# web3-testing — reviewed procedure

Adapted by OpenDigital from `wshobson/agents` at `9c61ab2`, `plugins/blockchain-web3/skills/web3-testing/SKILL.md#unit-testing-patterns,foundry-testing-forge`. See this domain’s PROVENANCE.yaml. This is a reviewed procedure, not an installed upstream tool or a validated runtime example.

Build fixtures against the actual contract ABI and pinned compiler/framework. Cover ownership/roles, initialization, transfers/accounting, events, failures, time/state transitions, boundary amounts and deployment/upgrade state where relevant.

Use current framework assertions for expected reverts; do not copy legacy testFail naming or examples with undeclared owner/addr1 variables and missing Token.sol. Add fuzzed inputs and sequence invariants, with explicit bounds and assumptions. Default to local chains. A fork needs a pinned block, authorized RPC, bounded resource use and no signing capability. This reference contains a test plan, not a claimed runnable token implementation.
