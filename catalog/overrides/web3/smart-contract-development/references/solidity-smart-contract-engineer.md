# Solidity Smart Contract Engineer — reviewed procedure

Adapted by OpenDigital from `msitarzewski/agency-agents` at `b859c51`, `engineering/engineering-solidity-smart-contract-engineer.md#security-first-development,code-quality,your-workflow-process`. See this domain’s PROVENANCE.yaml. This is a reviewed procedure, not an installed upstream tool or a validated runtime example.

Define asset flows, trust boundaries, privileged roles, upgrade/storage assumptions and invariants before choosing an implementation. Select library and compiler versions together; check their actual initialization and authorization model. Do not replace all authorization logic with an unqualified msg.sender rule.

Review external calls, state transitions, reentrancy, failures and events, then test intended and unauthorized behaviour, arithmetic limits, upgrade state and adversarial sequences. Choose coverage and gas criteria from risk and requirements rather than a universal percentage. Deployment, verification, role transfer and real-asset operations are separate authorized changes, never an automatic final step of this guide.

Consult the [Solidity security considerations](https://docs.soliditylang.org/en/latest/security-considerations.html) for the selected compiler version. Documentation and checklists cannot enumerate every vulnerability.
