# Godot Multiplayer Engineer — reviewed procedure

Adapted by OpenDigital from `msitarzewski/agency-agents` at `b859c51`, `game-development/godot/godot-multiplayer-engineer.md#critical-rules-you-must-follow,your-workflow-process`. See this domain’s PROVENANCE.yaml. This is a reviewed procedure, not an installed upstream tool or a validated runtime example.

Declare which peer owns each state transition and where authority is assigned during spawning. Client input is a request: validate sender identity, allowed state, sequence, rate and bounds at the authoritative peer. Replication is not authorization.

Choose reliable/unreliable delivery and synchronization from message semantics instead of marking every game event identically. Test joining late, disconnect/rejoin, packet loss, duplicate/out-of-order requests and impossible actions. Match MultiplayerSpawner, synchronizer and RPC configuration to the pinned Godot version. Use a local test topology and record authority/replication evidence without exposing credentials.
