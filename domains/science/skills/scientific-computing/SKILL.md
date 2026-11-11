---
name: scientific-computing
description: "Use when doing numerical or symbolic scientific computation: symbolic maths, units and uncertainty propagation, discrete-event or physical simulation (fluids, combustion, batteries), quantum circuits and open quantum systems, astronomy, geospatial analysis, multi-objective optimisation, graph analysis, large or chunked arrays and dataframes, MATLAB or Octave code, GPU acceleration or dataset versioning."
license: MIT
metadata:
  domain: science
  status: experimental
---
# Scientific computing

Compute results whose numbers can be trusted and reproduced.

## Procedure

1. **State the model:** equations, assumptions, units, boundary and initial conditions, and the quantity of interest.
2. **Carry units and uncertainty** through the calculation; convert at the edges, not in the middle.
3. **Start small:** a reduced problem with a known analytic or published answer; compare before scaling up.
4. **Check numerics:** convergence in step size or mesh, solver tolerances, conservation laws, stability; for stochastic methods, seeds and enough replications.
5. **Scale deliberately:** profile first; move to chunked, parallel or GPU execution only for the measured bottleneck, and verify the accelerated result against the reference run.
6. **Version data and code** together so a figure can be regenerated from a commit.

## Working rules

- **Pick one guide.** Load only the reference for the tool the task uses (list below). If two tools fit, say why you chose one.
- **Pin and record versions** of every library, model, database release and reference genome or dataset used; results depend on them.
- **Never fabricate data, results, identifiers or citations.** If a database query, file or run is unavailable, say so and stop at that step.
- **Run locally and boundedly.** Inspect inputs (shape, units, missing values, coordinate system, identifiers) before any transform; avoid jobs whose cost or duration you cannot estimate; ask before using paid services or cloud resources.
- **Validate before reporting:** sanity checks, controls, known reference values, or a re-run on a subset.
- **Report** the question, inputs (with versions and provenance), method and parameters, results with uncertainty, checks performed, and limitations. Keep scripts and seeds so the analysis can be reproduced.

## References

Load only what the task needs:

- `references/sympy/` — Performs exact symbolic mathematics with SymPy for algebra, calculus, equation solving, symbolic linear algebra, physics, and lambdify or LaTeX code generation. Use when a task nee
- `references/uncertainty-and-units/` — Tracks physical units and propagates measurement uncertainty in scientific calculations using pint and uncertainties. Use for unit conversion and dimensional checking, GUM uncertai
- `references/simpy/` — Builds, inspects, tests, and analyzes bounded process-based discrete-event simulations with SimPy. Use for event scheduling, resource queues, interrupts, monitoring, independent re
- `references/fluidsim/` — Plans, configures, inspects, restarts, and analyzes bounded FluidSim computational-fluid-dynamics simulations with explicit numerical-validity and HPC safety checks. Use for FluidS
- `references/cantera/` — Runs Cantera homogeneous chemical reactors and evaluates ignition delay with mechanism provenance, conservation checks, and numerical refinement. Use for combustion kinetics, close
- `references/pybamm/` — Simulates lithium-ion battery charge, discharge and rest experiments with PyBaMM, records parameter-set provenance, checks mesh and solver sensitivity, and compares predicted volta
- `references/qutip/` — Simulate and audit closed and open quantum-system models with QuTiP 5, including deterministic, trajectory, steady-state, spectral, and phase-space workflows. Use for local quantum
- `references/qiskit/` — Builds, simulates, transpiles, and executes quantum circuits with Qiskit and IBM Quantum Runtime. Use for Qiskit 2.x circuits and operators, V2 Sampler or Estimator primitives, tar
- `references/pennylane/` — Builds and differentiates PennyLane quantum circuits, hybrid PyTorch or JAX models, molecular VQE and QAOA workflows. Use for variational quantum algorithms, quantum machine learni
- `references/cirq/` — Google quantum computing framework. Use when targeting Google Quantum AI hardware, designing noise-aware circuits, or running quantum characterization experiments. Best for Google 
- `references/astropy/` — Core Python library for astronomy and astrophysics workflows that need Astropy APIs, including units/quantities, coordinates, FITS I/O, tables, time systems, WCS, and cosmology. Us
- `references/marine-carbonate-chemistry/` — Solves seawater carbonate chemistry with PyCO2SYS for chemical oceanography, ocean acidification, and marine carbon-cycle research. Use for paired total alkalinity, dissolved inorg
- `references/openpiv/` — Performs Particle Image Velocimetry (PIV) analysis with OpenPIV. Use when extracting velocity fields from PIV image pairs, analyzing fluid dynamics or flow visualization experiment
- `references/matlab/` — Builds, reviews, migrates, and plans MATLAB or GNU Octave numerical workflows. Use for arrays, tabular/time data, tests, projects, graphics, MAT files, and explicit Python interope
- `references/optimize-for-gpu/` — GPU-accelerates scientific Python on NVIDIA hardware and verifies that the result is correct and faster. Use for CUDA/GPU optimization; CPU-bound NumPy, SciPy, pandas, scikit-learn
- `references/dask/` — Scales pandas, NumPy, and custom Python research workflows beyond memory or across clusters with Dask. Covers DataFrames, Arrays, Bags, Futures, chunking, schedulers, and distribut
- `references/zarr-python/` — Stores and queries chunked N-D scientific arrays with Zarr-Python 3, including codecs, sharding, S3/GCS storage, and NumPy/Dask/Xarray integration. Use for array layout, bounded I/
- `references/vaex/` — Processes large tabular scientific datasets with Vaex expressions, filtered views, streamed statistics, binned visualizations, and file conversion. Use for larger-than-RAM HDF5, Ar
- `references/polars/` — High-performance DataFrame library for Python ETL, analytics, and pandas migration. It supports expression-based data manipulation with lazy query optimization, parallel execution,
- `references/pymoo/` — Solves and validates single-, multi-, and many-objective optimization with pymoo, including NSGA-II, NSGA-III, MOEA/D, constraints, Pareto approximations, reference directions, and
- `references/networkx/` — Creates, analyzes, and visualizes complex networks and graphs in Python with NetworkX. Use when working with network/graph data structures, computing graph algorithms (shortest pat
- `references/geopandas/` — Guidance and local audit tools for Python workflows that directly use GeoPandas GeoSeries, GeoDataFrame, spatial operations, or vector-data I/O.
- `references/geomaster/` — Supports geospatial research workflows for remote sensing, vector and raster GIS, spatial statistics, terrain and network analysis, and machine learning for Earth observation. Use 
- `references/datalad/` — Retrieves, versions, and publishes scientific datasets with DataLad and git-annex, and captures computational provenance with datalad run, rerun, and containers-run. Use when cloni
