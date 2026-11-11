---
name: cheminformatics
description: "Use when working with small molecules, proteins or materials computationally: parsing and standardising SMILES or SDF, descriptors and fingerprints, similarity and substructure search, drug-likeness filters, property prediction, docking, molecular dynamics, mass spectra or NMR processing, protein language models, crystal structures or phase equilibria."
license: MIT
metadata:
  domain: science
  status: experimental
---
# Cheminformatics

Compute on molecules and materials with traceable, chemically valid inputs.

## Procedure

1. **Standardise structures first:** sanitise, neutralise or keep charges deliberately, handle tautomers and stereochemistry, strip salts; record the toolkit and version. Reject what cannot be parsed instead of guessing.
2. **Choose representations** for the question (fingerprint type and radius, descriptors, 3D conformers, graphs) and keep them fixed across compared sets.
3. **Split data honestly** for models: scaffold or time splits for prospective claims, not only random splits.
4. **Simulate within known limits:** docking scores rank poses, they are not binding affinities; MD needs equilibration and convergence checks; force fields and functionals must suit the system.
5. **Check against references:** known actives, crystal poses, literature values, or experimental spectra.

## Working rules

- **Pick one guide.** Load only the reference for the tool the task uses (list below). If two tools fit, say why you chose one.
- **Pin and record versions** of every library, model, database release and reference genome or dataset used; results depend on them.
- **Never fabricate data, results, identifiers or citations.** If a database query, file or run is unavailable, say so and stop at that step.
- **Run locally and boundedly.** Inspect inputs (shape, units, missing values, coordinate system, identifiers) before any transform; avoid jobs whose cost or duration you cannot estimate; ask before using paid services or cloud resources.
- **Validate before reporting:** sanity checks, controls, known reference values, or a re-run on a subset.
- **Report** the question, inputs (with versions and provenance), method and parameters, results with uncertainty, checks performed, and limitations. Keep scripts and seeds so the analysis can be reproduced.

## References

Load only what the task needs:

- `references/rdkit/` — Cheminformatics toolkit for fine-grained molecular control. SMILES/SDF parsing, descriptors (MW, LogP, TPSA), fingerprints, substructure search, 2D/3D generation, similarity, react
- `references/datamol/` — Pythonic wrapper around RDKit with simplified interface and sensible defaults. Preferred for standard drug discovery including SMILES parsing, standardization, descriptors, fingerp
- `references/molfeat/` — Featurizes small molecules with Molfeat for QSAR/QSPR, chemical similarity, virtual screening, and molecular ML. Covers ECFP/MACCS fingerprints, RDKit descriptors, pharmacophores, 
- `references/medchem/` — Applies medicinal chemistry filters for compound triage, using drug-likeness rules (Lipinski, Veber, CNS), structural alert catalogs (PAINS, NIBR, ChEMBL), complexity metrics, and 
- `references/deepchem/` — Builds molecular property prediction and MoleculeNet workflows with DeepChem, including SMILES featurization, scaffold or grouped holdouts, masked labels, graph models and explicit
- `references/diffdock/` — Predicts protein-small-molecule binding poses with DiffDock and DiffDock-L from PDB or sequence plus SMILES/SDF/MOL2. Covers batch docking, pose triage, confidence interpretation, 
- `references/molecular-dynamics/` — Runs and analyzes molecular dynamics simulations with OpenMM and MDAnalysis. Sets up protein/small molecule systems, defines force fields, runs energy minimization and production M
- `references/pytdc/` — Provides Therapeutics Data Commons workflows through PyTDC for registry discovery, dataset access, task-aware splits, evaluator metrics, benchmark groups, and bounded molecular-ora
- `references/torchdrug/` — Builds and troubleshoots TorchDrug 0.2.1 workflows for molecular graphs, property prediction, self-supervised pretraining, molecule generation, retrosynthesis, protein representati
- `references/matchms/` — Processes, cleans, compares, and searches tandem mass spectra with matchms. Use for MS/MS file I/O, metadata harmonization, peak filtering, spectral similarity, library matching, s
- `references/pyopenms/` — Processes mass spectrometry data with pyOpenMS. Supports proteomics and metabolomics workflows—feature detection, peptide/protein identification, label-free quantification, adduct/
- `references/nmrglue/` — Processes calibrated one-dimensional complex NMR free-induction decays with nmrglue into phased spectra, peak candidates, and signed integration regions. Use for raw 1D NMR process
- `references/esm/` — Uses the Biohub esm Python SDK for ESM3 protein generation, ESMC embeddings, and ESMFold2 all-atom folding. Applies to local model inference and Biohub hosted clients, including fo
- `references/pymatgen/` — Analyzes, validates, converts, and transforms materials structures and computed materials data with pymatgen. Use for local phase diagrams, symmetry sensitivity, electronic-structu
- `references/pycalphad/` — Computes finite-temperature CALPHAD equilibria, phase fractions, and phase compositions from thermodynamic TDB databases using pycalphad. Use for alloy phase stability, equilibrium
