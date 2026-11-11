---
name: lab-automation
description: "Use when automating laboratory work: writing or reviewing liquid-handling protocols for Opentrons or PyLabRobot, simulating runs before hardware, exporting and validating protocols from protocols.io, or designing parametric lab hardware for fabrication."
license: MIT
metadata:
  domain: science
  status: experimental
---
# Lab automation

Turn a bench procedure into an automated protocol that is safe to run.

## Procedure

1. **Write down the manual protocol** first: labware, volumes, reagents, order, incubation and mixing steps, and acceptance criteria.
2. **Map to hardware:** deck layout, labware definitions, pipettes and tip usage; check volume ranges and tip counts before writing code.
3. **Simulate** every protocol before a hardware run and review the simulated steps and tip usage.
4. **First run dry,** then with water, then with real reagents; a person supervises the first real run.
5. **Version the protocol** and record the robot software version and calibration state with each run.
6. **Physical hardware:** export designs with tolerances and material notes; never claim fitness for safety-critical use.

## Working rules

- **Pick one guide.** Load only the reference for the tool the task uses (list below). If two tools fit, say why you chose one.
- **Pin and record versions** of every library, model, database release and reference genome or dataset used; results depend on them.
- **Never fabricate data, results, identifiers or citations.** If a database query, file or run is unavailable, say so and stop at that step.
- **Run locally and boundedly.** Inspect inputs (shape, units, missing values, coordinate system, identifiers) before any transform; avoid jobs whose cost or duration you cannot estimate; ask before using paid services or cloud resources.
- **Validate before reporting:** sanity checks, controls, known reference values, or a re-run on a subset.
- **Report** the question, inputs (with versions and provenance), method and parameters, results with uncertainty, checks performed, and limitations. Keep scripts and seeds so the analysis can be reproduced.

## References

Load only what the task needs:

- `references/opentrons-integration/` — Authors, reviews, migrates, simulates, and troubleshoots official Opentrons Python Protocol API v2 protocols for Flex and OT-2 robots. Use for robot-specific liquid handling, deck 
- `references/pylabrobot/` — Develops and reviews PyLabRobot lab-automation resources, liquid-handling plans, offline simulations, and supported-device integrations. Supports PyLabRobot protocols and API quest
- `references/protocolsio-integration/` — Reads, validates, and safely exports protocols.io data with current official REST/MCP contracts, or creates non-executing mutation plans. The bundled client makes bounded official-
- `references/lab-hardware-cad/` — Designs custom laboratory hardware as parametric build123d models and exports fabrication artifacts as STEP, STL, and DXF files - microfluidic chips and molds, optomechanical mount
