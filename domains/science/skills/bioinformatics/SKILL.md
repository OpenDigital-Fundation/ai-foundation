---
name: bioinformatics
description: "Use when analysing biological sequence or omics data: single-cell or bulk RNA-seq, genomic intervals and variants, CRISPR screens, amplicon and microbiome reads, gene regulatory networks, pathway enrichment, primer design, metabolic or kinetic models, workflow pipelines (Nextflow) or querying public biological databases."
license: MIT
metadata:
  domain: science
  status: experimental
---
# Bioinformatics

Turn raw or processed biological data into a defensible result.

## Procedure

1. **Frame the question** as a comparison or estimate (e.g. "genes differentially expressed between conditions, controlling for batch"). Name organism, assembly (GRCh38, GRCm39…), annotation release and sample design.
2. **Inspect inputs:** file formats (FASTQ, BAM/CRAM, VCF, BED, h5ad, count matrices), coordinate convention (0- or 1-based, half-open), identifiers (Ensembl, symbols, UniProt), and sample metadata. Convert coordinates and identifiers explicitly.
3. **Quality control** before analysis: read and cell QC, doublets, mitochondrial fraction, library size, batch structure. Record thresholds.
4. **Analyse** with the standard tool for the data type (guides below), keeping defaults unless there is a reason to change them, and recording every non-default parameter.
5. **Correct for multiplicity and batch** where relevant (FDR, design formulas, integration methods) and keep raw counts for statistics.
6. **Interpret** with enrichment or databases only after the primary result is fixed; state the background set and the database release.

## Working rules

- **Pick one guide.** Load only the reference for the tool the task uses (list below). If two tools fit, say why you chose one.
- **Pin and record versions** of every library, model, database release and reference genome or dataset used; results depend on them.
- **Never fabricate data, results, identifiers or citations.** If a database query, file or run is unavailable, say so and stop at that step.
- **Run locally and boundedly.** Inspect inputs (shape, units, missing values, coordinate system, identifiers) before any transform; avoid jobs whose cost or duration you cannot estimate; ask before using paid services or cloud resources.
- **Validate before reporting:** sanity checks, controls, known reference values, or a re-run on a subset.
- **Report** the question, inputs (with versions and provenance), method and parameters, results with uncertainty, checks performed, and limitations. Keep scripts and seeds so the analysis can be reproduced.

Further detail files of the merged guides:

- [`references/genomic-coordinates/references/reference-builds.md`](references/genomic-coordinates/references/reference-builds.md)

## References

Load only what the task needs:

- `references/scanpy/` — Performs Scanpy single-cell RNA-seq QC, normalization, HVG selection, PCA/UMAP/t-SNE, clustering, exploratory marker ranking, pseudobulk preparation, visualization, and Seurat or S
- `references/anndata/` — Handles annotated matrices in single-cell analysis, .h5ad and Zarr files, and integration with the scverse ecosystem. This is the data format skill—for analysis workflows use scanp
- `references/scvi-tools/` — Fits probabilistic models for single-cell omics, including scVI batch integration, scANVI annotation, totalVI CITE-seq, MultiVI RNA/ATAC integration, and posterior differential exp
- `references/scvelo/` — Performs RNA velocity analysis with scVelo from spliced and unspliced single-cell RNA counts. Fits deterministic or dynamical models, examines gene phase portraits, builds velocity
- `references/cellxgene-census/` — Queries the CZ CELLxGENE Census programmatically for versioned public single-cell and spatial transcriptomics data. Use when you need population-scale cell metadata, gene expressio
- `references/bulk-rnaseq/` — Prepares bulk RNA-seq FASTQ, Salmon, STAR or featureCounts output for gene-level differential expression. Covers nf-core/rnaseq and standalone quantification, biological replicatio
- `references/pydeseq2/` — Performs bulk RNA-seq differential expression analysis with PyDESeq2, including count validation, formula designs, explicit contrasts, Wald tests, FDR correction, coefficient-match
- `references/pysam/` — Provides Python/HTSlib workflows for genomic files. Used when reading, querying, filtering, or writing SAM/BAM/CRAM, VCF/BCF, FASTA/FASTQ, or tabix data with pysam, including pileu
- `references/genomic-coordinates/` — Converts genomic intervals between coordinate conventions, normalises and compares variant representations, and detects assembly or contig-naming mismatches before they corrupt an 
- `references/gtars/` — Supports Gtars for local genomic interval models and set algebra, overlaps and counts, consensus and coverage, tokenization, fragment processing, and refget/BEDbase planning across
- `references/polars-bio/` — Performs genomic interval overlap, nearest, merge, coverage, complement and subtraction on Polars DataFrames, and reads or writes BED, VCF, BCF, BAM, CRAM, GFF, GTF, FASTA and FAST
- `references/geniml/` — Supports audited local Geniml genomic-interval workflows: validate BED and universe contracts, plan Region2Vec or scEmbed runs, inspect model/tokenizer compatibility, and assess co
- `references/deeptools/` — NGS analysis toolkit. BAM to bigWig conversion, QC (correlation, PCA, fingerprints), heatmaps/profiles (TSS, peaks), for ChIP-seq, RNA-seq, ATAC-seq visualization.
- `references/arboreto/` — Infers candidate gene regulatory networks from bulk or single-cell expression data using AertsLab Arboreto GRNBoost2 and GENIE3. Use for transcription factor-target association ran
- `references/mageck/` — Analyzes pooled CRISPR screen FASTQ reads and guide-count matrices with MAGeCK, validates guide libraries and contrasts, measures replicate and library QC, and produces gene hit ra
- `references/pathway-enrichment/` — Performs pathway and gene-set enrichment analysis on gene lists or ranked gene data and interprets the results. Used when the user has a set of genes (differentially expressed gene
- `references/qiime2-amplicon/` — Processes paired-end 16S amplicon reads into QIIME 2 ASVs and taxonomy with retained artifact provenance. Checks paired FASTQ manifests, primer orientation diagnostics, predicted p
- `references/primer-design/` — Designs and audits PCR and RT-qPCR primers with Primer3, explicit thermodynamic conditions, reference-based off-target amplification searches, and traceable sequence coordinates. U
- `references/biopython/` — Provides Biopython workflows for sequence manipulation, file parsing (FASTA/GenBank/PDB), phylogenetics, and programmatic NCBI/PubMed access (Bio.Entrez). Supports batch processing
- `references/gget/` — Queries 20+ bioinformatics resources through CLI/Python. Supports quick lookups of gene info, BLAST/BLAT, viral sequence downloads, PDB/mmCIF structures, G2P residue annotations, e
- `references/scikit-bio/` — Biological data toolkit. Sequence analysis, alignments, phylogenetic trees, diversity metrics (alpha/beta, UniFrac), ordination (PCoA), PERMANOVA, FASTA/Newick I/O, for microbiome 
- `references/nextflow/` — Builds, runs, and debugs Nextflow DSL2 pipelines and nf-core workflows. Use for Nextflow, nf-core, .nf files, nextflow.config, processes/channels/operators, samplesheets, nf-test, 
- `references/tiledbvcf/` — Stores and retrieves genomic variant calls with TileDB-VCF. Use for indexed single-sample VCF/BCF ingestion, incremental cohorts, region and sample queries, streaming results, alle
- `references/alphagenome/` — Looks up precomputed AlphaGenome Atlas effects for any GRCh38 single-nucleotide variant (AVI score with Phred and 18 SHAP feature attributions, plus raw and quantile scores for RNA
- `references/onekgpd/` — Queries the 1000 Genomes Project dataset (3,202 whole-genome-sequenced
- `references/pathogen-variant-surveillance/` — Queries public GenSpectrum LAPIS data for pathogen genomic surveillance, current lineage nomenclature, weekly sequence proportions, reporting delays, and descriptive mutation frequ
- `references/ontology-term-resolution/` — Resolves free-text scientific labels to ontology term IDs and validates existing CURIEs against the EBI Ontology Lookup Service (OLS4). Also looks up prefixes in Bioregistry, resol
- `references/13c-metabolic-flux/` — Estimates intracellular metabolic fluxes from steady-state carbon-13 isotope-tracing measurements using validated atom maps, mfapy isotope simulation, constrained multistart fittin
- `references/tellurium/` — Simulates biochemical kinetic models from SBML or Antimony with Tellurium and libRoadRunner, checks model units, compares deterministic parameter perturbations, and exports and rep
- `references/lamindb/` — Manages biological datasets and models with LaminDB, including artifact registration, lineage tracking, schema validation, Bionty ontology annotation, query/search, collections, br
- `references/database-lookup/` — Queries documented public database APIs with explicit endpoints, filters, pagination, and provenance. Used when a scientific, regulatory, financial, or other database-backed fact m
- `references/pacsomatic/` — Prepares and launches nf-core/pacsomatic matched tumor-normal PacBio HiFi genomics workflows from unaligned BAM inputs. Supports samplesheet generation, pinned Nextflow launch arti
- `references/genomic-intelligence/` — Predicts regulatory features, gene structure, and expression directly from DNA sequence using Genomic Intelligence's hosted transformer DNA language models — no local GPU or model 
