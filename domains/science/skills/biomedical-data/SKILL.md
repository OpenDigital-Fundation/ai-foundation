---
name: biomedical-data
description: "Use when processing biomedical research data: DICOM images, whole-slide pathology, microscopy pipelines and OMERO, flow cytometry files, physiological signals, Neuropixels electrophysiology, Neurodata Without Borders conversion, cryo-EM refinement or public cancer imaging collections. Research use only, not clinical decisions."
license: MIT
metadata:
  domain: science
  status: experimental
---
# Biomedical research data

Handle biomedical research data correctly, safely and reproducibly.

## Procedure

1. **Confirm the purpose is research.** This skill does not support diagnosis or treatment decisions; say so if asked.
2. **Protect identities:** check for personal or health data in headers, filenames and metadata (DICOM tags, slide labels); de-identify or stop before sharing.
3. **Read metadata first:** acquisition parameters, pixel spacing, channels, sampling rate, compensation matrices and units.
4. **Process with documented pipelines** (guides below), keeping raw data unchanged and writing outputs to new files.
5. **Quality-check outputs** visually and quantitatively (segmentation overlays, spike sorting metrics, gating plots, resolution estimates).
6. **Respect data-use terms** of public collections; many carry their own licences per collection.

## Working rules

- **Pick one guide.** Load only the reference for the tool the task uses (list below). If two tools fit, say why you chose one.
- **Pin and record versions** of every library, model, database release and reference genome or dataset used; results depend on them.
- **Never fabricate data, results, identifiers or citations.** If a database query, file or run is unavailable, say so and stop at that step.
- **Run locally and boundedly.** Inspect inputs (shape, units, missing values, coordinate system, identifiers) before any transform; avoid jobs whose cost or duration you cannot estimate; ask before using paid services or cloud resources.
- **Validate before reporting:** sanity checks, controls, known reference values, or a re-run on a subset.
- **Report** the question, inputs (with versions and provenance), method and parameters, results with uncertainty, checks performed, and limitations. Keep scripts and seeds so the analysis can be reproduced.

Further detail files of the merged guides:

- [`references/nwb-conversion/references/upstream-review.md`](references/nwb-conversion/references/upstream-review.md)

## References

Load only what the task needs:

- `references/pydicom/` — Reads, inspects, writes, transforms, and preflights local DICOM datasets and pixel data. Applies to DICOM metadata, transfer syntaxes, compression plugins, frames, private elements
- `references/histolab/` — Extracts and preprocesses whole-slide histology image tiles with Histolab. Use for WSI inspection, tissue masks, random/grid/score-based tile extraction, H&E stain normalization, a
- `references/pathml/` — Supports local computational pathology research with PathML: slide loading and tiling, preprocessing and QC, h5path storage, multiplex quantification, spatial graphs, and bounded m
- `references/neurokit2/` — Builds and audits reproducible NeuroKit2 research workflows for physiological time-series preprocessing, event/interval analysis, multimodal alignment, variability, and complexity.
- `references/neuropixels-analysis/` — Analyzes Neuropixels extracellular recordings end-to-end with SpikeInterface. Covers loading SpikeGLX/Open Ephys/NWB data, preprocessing, drift/motion correction, Kilosort4 (and CP
- `references/nwb-conversion/` — Converts neuroscience acquisition data to Neurodata Without Borders files with NeuroConv and PyNWB, preserves metadata and timebases, checks evidence-based clock alignment, and pro
- `references/flowio/` — Reads, inspects, and writes Flow Cytometry Standard (FCS) 2.0, 3.0, and 3.1 files with FlowIO. Use for low-level FCS metadata and channel inspection, NumPy event extraction, multi-
- `references/flowkit/` — Analyzes flow cytometry data with FlowKit, including spillover compensation, logicle and biexponential transforms, hierarchical gating, GatingML strategies, and supported FlowJo 10
- `references/relion/` — Validates and executes RELION single-particle cryo-EM refinement and half-map postprocessing. Supports STAR optics/acquisition checks, particle-stack consistency, gold-standard hal
- `references/cellprofiler/` — Runs reproducible CellProfiler microscopy pipelines for nuclear segmentation, cell counts, and per-object fluorescence measurements. Supports image/channel manifests, headless batc
- `references/omero-integration/` — Inspects and automates microscopy data workflows against OMERO.server with omero-py, BlitzGateway, OMERO CLI, tables, annotations, ROIs, rendering, and documented OMERO.web APIs. U
- `references/imaging-data-commons/` — Queries and downloads public cancer imaging data from NCI Imaging Data Commons. Supports IDC collection discovery, DICOM access, radiology (CT, MR, PET) and pathology AI datasets, 
