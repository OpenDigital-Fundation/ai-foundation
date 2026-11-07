# `code-quality`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

Evaluating and improving existing code - giving and receiving review, simplification, refactoring, debt, repository audits.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install code-quality@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### agent

| Artefato | Estado | Quando usar |
|---|---|---|
| [`code-reviewer`](agents/code-reviewer.md) | experimental | Read-only reviewer with a fresh context. Use to review a diff, branch, pull request or completed plan task against its spec and the repository's standards, and report numbered, evidence-backed findings with a verdict. D… |

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`code-review`](skills/code-review/SKILL.md) | experimental | Use when a change needs review - after finishing a plan task or feature, before merging, when stuck, or when the user asks to review a diff, commit, branch or pull request. Pins the range, finds the spec and the reposit… |
| [`codebase-audit`](skills/codebase-audit/SKILL.md) | experimental | Use when the user asks for a thorough review or audit of a whole codebase, a branch or diff, or a folder - "audit this repo", "review the whole project", "find vulnerabilities", "find duplicated code", "optimise the cod… |
| [`debt-ledger`](skills/debt-ledger/SKILL.md) | experimental | Use when the user asks what was deferred, which shortcuts exist, or for a technical-debt ledger. Collects every `shortcut: <limit>, <when to upgrade>` comment (or a marker the user names) into one ranked ledger. Report… |
| [`receiving-code-review`](skills/receiving-code-review/SKILL.md) | experimental | Use when receiving code review feedback, before implementing any suggestion, especially when a finding seems unclear or technically questionable. Verifies each finding against the code, asks when unclear, pushes back wi… |
| [`simplification`](skills/simplification/SKILL.md) | experimental | Use when existing code should get simpler without changing behaviour: removing dead code and unused exports, collapsing needless abstraction, clarifying names and types, cleaning comments, and refactoring safely behind… |

## Origem e manutenção

- Entrada editorial: [manifesto de `code-quality`](../../catalog/curation/domains/code-quality.yaml).
- Requisitos: [spec do domínio](../../docs/specs/code-quality/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/code-quality/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `code-reviewer` | affaan-m/ECC, msitarzewski/agency-agents, obra/superpowers |
| `code-review` | Community-Access/accessibility-agents, DietrichGebert/ponytail, affaan-m/ECC, mattpocock/skills, obra/superpowers |
| `codebase-audit` | DietrichGebert/ponytail, affaan-m/ECC |
| `debt-ledger` | DietrichGebert/ponytail |
| `receiving-code-review` | obra/superpowers |
| `simplification` | affaan-m/ECC |
