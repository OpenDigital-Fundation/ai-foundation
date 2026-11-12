# Roblox Systems Scripter — reviewed procedure

Adapted by OpenDigital from `msitarzewski/agency-agents` at `b859c51`, `game-development/roblox-studio/roblox-systems-scripter.md#critical-rules-you-must-follow,your-workflow-process`. See this domain’s PROVENANCE.yaml. This is a reviewed procedure, not an installed upstream tool or a validated runtime example.

Separate server-authoritative gameplay/persistence from client presentation and prediction. Validate the actual sender, permission, state, bounds and rate of each remote request. A server-originated message does not make arbitrary payloads automatically safe.

Design persistence keys, schema versions, conflict handling, bounded retries and shutdown behaviour against the current DataStore limits; do not hardcode a generic save interval as a platform guarantee. Keep module initialization and cleanup explicit. Test invalid remote input, repeated requests, disconnects, failed persistence and concurrent updates in authorized test environments.
