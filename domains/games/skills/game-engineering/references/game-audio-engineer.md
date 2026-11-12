# Game Audio Engineer — reviewed procedure

Adapted by OpenDigital from `msitarzewski/agency-agents` at `b859c51`, `game-development/game-audio-engineer.md#integration-standards,memory-and-voice-budget,spatial-audio,your-workflow-process`. See this domain’s PROVENANCE.yaml. This is a reviewed procedure, not an installed upstream tool or a validated runtime example.

Define event names, parameters, routing/buses, ownership and lifecycle for gameplay-driven sound. Middleware is an option, not a requirement; engine-native playback may fit the project. Establish voice priorities, stealing behaviour, memory and streaming policies for target hardware and actual assets.

Test repeated triggers, scene changes, mute/settings, occlusion, transitions and maximum simultaneous events. Select compression, spatialization and streaming from measured latency, quality and resource use rather than universal duration/format rules. Offer visual or other alternatives for important audio-only information. Deliver an event/parameter map and measured stress-test results.
