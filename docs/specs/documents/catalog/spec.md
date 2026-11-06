# Spec — Catálogo do domínio `documents`

- **Domínio:** documents
- **Status:** em implementação (Onda 2)
- **Fronteira:** documentos de escritório e escrita técnica/corporativa.

## Resultado (gerado por `tools.curation.bundle` a partir de [`bundles/knowledge-work.yaml`](../../../../catalog/decisions/bundles/knowledge-work.yaml))

| Artefato | Base | Referências |
|---|---|---|
| `office-documents` | procedimento original | `specialized-document-generator` |
| `doc-coauthoring` | anthropics/skills `doc-coauthoring` | — |
| `technical-writing` | `engineering-technical-writer` | `doc-updater` |
| `internal-comms` | anthropics/skills `internal-comms` | — |

- `docx`, `xlsx`, `pptx`, `pdf` da Anthropic são proprietárias: `office-documents` só orienta a instalá-las da fonte oficial e oferece um fluxo alternativo com bibliotecas livres.
- mattpocock `writing-fragments`/`writing-beats`/`writing-shape` excluídos (marcados como em andamento no upstream).

## Pendências

- ECC `article-writing` e agency *Book Co-Author*, *Grant Writer*, *Language Translator*: decidir entre `documents` e `marketing`.
