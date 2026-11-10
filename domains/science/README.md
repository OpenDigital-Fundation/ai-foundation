# `science`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

Computational science - omics, chemistry, simulation, study design and statistics, scientific writing, biomedical research data, lab automation.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install science@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`bioinformatics`](skills/bioinformatics/SKILL.md) | experimental | Use when analysing biological sequence or omics data: single-cell or bulk RNA-seq, genomic intervals and variants, CRISPR screens, amplicon and microbiome reads, gene regulatory networks, pathway enrichment, primer desi… |
| [`biomedical-data`](skills/biomedical-data/SKILL.md) | experimental | Use when processing biomedical research data: DICOM images, whole-slide pathology, microscopy pipelines and OMERO, flow cytometry files, physiological signals, Neuropixels electrophysiology, Neurodata Without Borders co… |
| [`cheminformatics`](skills/cheminformatics/SKILL.md) | experimental | Use when working with small molecules, proteins or materials computationally: parsing and standardising SMILES or SDF, descriptors and fingerprints, similarity and substructure search, drug-likeness filters, property pr… |
| [`experimental-design`](skills/experimental-design/SKILL.md) | experimental | Use when planning or analysing a study: forming hypotheses and rival explanations, choosing a design, randomisation and blinding, sample size and power, choosing and checking statistical tests or models (regression, mix… |
| [`lab-automation`](skills/lab-automation/SKILL.md) | experimental | Use when automating laboratory work: writing or reviewing liquid-handling protocols for Opentrons or PyLabRobot, simulating runs before hardware, exporting and validating protocols from protocols.io, or designing parame… |
| [`scientific-computing`](skills/scientific-computing/SKILL.md) | experimental | Use when doing numerical or symbolic scientific computation: symbolic maths, units and uncertainty propagation, discrete-event or physical simulation (fluids, combustion, batteries), quantum circuits and open quantum sy… |
| [`scientific-writing`](skills/scientific-writing/SKILL.md) | experimental | Use when writing or reviewing scientific work: manuscripts and reports in IMRaD or journal formats, peer-review reports, grant proposals, venue and journal templates, posters, research talks and publication-quality figu… |

## Origem e manutenção

- Entrada editorial: [manifesto de `science`](../../catalog/curation/domains/science.yaml).
- Requisitos: [spec do domínio](../../docs/specs/science/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/science/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `bioinformatics` | K-Dense-AI/claude-scientific-skills |
| `biomedical-data` | K-Dense-AI/claude-scientific-skills |
| `cheminformatics` | K-Dense-AI/claude-scientific-skills |
| `experimental-design` | K-Dense-AI/claude-scientific-skills |
| `lab-automation` | K-Dense-AI/claude-scientific-skills |
| `scientific-computing` | K-Dense-AI/claude-scientific-skills |
| `scientific-writing` | K-Dense-AI/claude-scientific-skills |
