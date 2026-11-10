---
name: experimental-design
description: "Use when planning or analysing a study: forming hypotheses and rival explanations, choosing a design, randomisation and blinding, sample size and power, choosing and checking statistical tests or models (regression, mixed, Bayesian, survival), exploratory analysis, validating an analytical method, or critically appraising the evidence behind a scientific claim."
license: MIT
metadata:
  domain: science
  status: experimental
---
# Experimental design

Design studies that can answer their question, and analyse them without fooling yourself.

## Procedure

1. **Question and hypotheses:** primary question, primary outcome, the effect that would matter in practice, and rival explanations to rule out.
2. **Design before data:** unit of analysis, controls, randomisation, blinding, confounders, and how missing data will be handled. Write the analysis plan before seeing outcomes.
3. **Size the study** with a power analysis from a justified effect size; report the assumptions.
4. **Explore without testing:** describe distributions, outliers and data quality; keep exploratory findings labelled as such.
5. **Analyse as planned:** check model assumptions, use the pre-specified test or model, correct for multiple comparisons, and report effect sizes with intervals, not only p-values.
6. **Appraise the evidence:** design limitations, bias, reproducibility, and what result would change the conclusion.

## Working rules

- **Pick one guide.** Load only the reference for the tool the task uses (list below). If two tools fit, say why you chose one.
- **Pin and record versions** of every library, model, database release and reference genome or dataset used; results depend on them.
- **Never fabricate data, results, identifiers or citations.** If a database query, file or run is unavailable, say so and stop at that step.
- **Run locally and boundedly.** Inspect inputs (shape, units, missing values, coordinate system, identifiers) before any transform; avoid jobs whose cost or duration you cannot estimate; ask before using paid services or cloud resources.
- **Validate before reporting:** sanity checks, controls, known reference values, or a re-run on a subset.
- **Report** the question, inputs (with versions and provenance), method and parameters, results with uncertainty, checks performed, and limitations. Keep scripts and seeds so the analysis can be reproduced.

## References

Load only what the task needs:

- `references/experimental-design/` — Designs experiments and studies BEFORE data is collected — choosing a design, randomizing, blocking, and laying out treatment combinations so results are interpretable. Use wheneve
- `references/statistical-power/` — Calculates sample sizes and statistical power for study planning. Applies when someone asks "how many subjects/samples/replicates do I need", wants an a priori power analysis, a mi
- `references/statistical-analysis/` — Guided statistical analysis for research data - test selection, assumption checking, effect sizes, power analysis, Bayesian alternatives, and APA-formatted reporting. Use whenever 
- `references/statsmodels/` — Fits and diagnoses Python statistical models including OLS, GLM, discrete and mixed models, ARIMA and SARIMAX. Supports coefficient inference, marginal effects, model comparison an
- `references/pymc/` — Builds and checks Bayesian models with PyMC, including hierarchical models, NUTS MCMC, variational inference, mutable-data predictions, posterior predictive checks, diagnostics, an
- `references/scikit-survival/` — Builds, evaluates, and audits right-censored or competing-risk survival workflows with scikit-survival, including leakage-safe preprocessing, model selection, probability predictio
- `references/exploratory-data-analysis/` — Performs bounded, local exploratory analysis of explicitly supported scientific files. Supports redacted CSV/TSV/JSON profiles; optional NumPy, HDF5, FASTA/FASTQ, and basic image m
- `references/analytical-method-validation/` — Plans, executes, and documents validation, verification, and transfer of analytical procedures under the governing framework - ICH Q2(R2) and Q14, USP <1220>/<1225>/<1226>, ICH M10
- `references/hypothesis-generation/` — Formulates evidence-bounded scientific questions, candidate hypotheses, rival explanations, causal or associational claims, discriminating predictions, measurements, and preregistr
- `references/scientific-critical-thinking/` — Evaluates scientific claims and evidence quality. Applies to experimental design validity, biases and confounders, statistical interpretation, evidence grading frameworks (GRADE, C
- `references/scientific-brainstorming/` — Facilitates evidence-aware scientific ideation with independent generation, structured discussion, explicit assumptions, transparent evaluation, adversarial review, and decision lo
