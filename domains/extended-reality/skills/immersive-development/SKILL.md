---
name: immersive-development
description: "Use when designing or implementing AR, VR or XR applications: spatial reference frames, tracked input, immersive interaction, comfort, rendering budgets and runtime fallbacks."
license: MIT
metadata:
  domain: extended-reality
  status: experimental
---
# Immersive development

## Select the experience contract
Identify headset/browser/runtime and supported versions, AR versus VR, seated/standing/room-scale use, input capabilities, environmental constraints and accessibility needs. Treat tracking and spatial data as potentially sensitive.

## Develop and evaluate
1. Define coordinate units, handedness, reference spaces, origin resets and transform ownership. Test known real-world distances instead of assuming an engine unit is a metre.
2. Specify the interaction state machine for gaze, controllers, hands or other supported inputs. Include focus, selection, cancellation, lost tracking, re-entry and fallback controls.
3. For cockpit or constrained experiences, anchor reachable controls and avoid unintended camera motion. Expose appropriate comfort choices; none guarantees absence of motion sickness.
4. Derive frame-time, memory and thermal budgets from the chosen runtime/device. Measure representative workloads; fixed universal FPS tables are not acceptance evidence.
5. Handle permission denial, absent features, tracking loss, session interruption and non-immersive fallback without exposing private sensor data.
6. Validate readable scale/depth, reach, occlusion, input alternatives and comfort with suitable participants and a safe physical setup. Record device/runtime and limitations.

## Deliverable
An interaction/reference-space contract, prototype, device test matrix, performance traces and fallback behaviour. Native visionOS/RealityKit and browser WebXR are alternative implementations, not universal dependencies. Game mechanics belong to games; reusable UI styling and research methods stay in ui/ux.

## References

Load only what the task needs:

- [`references/vr-ar.md`](references/vr-ar.md) — Reviewed adaptation: vr-ar; version and approval assumptions are explicit.
