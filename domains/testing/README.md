# `testing`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

Proving behaviour - TDD, test strategy, end-to-end and browser testing, verification before completion.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install testing@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`browser-testing`](skills/browser-testing/SKILL.md) | experimental | Use when testing a web application in a real browser: driving a local app with Playwright, writing or stabilising end-to-end tests, Page Objects, capturing screenshots and console logs, post-deploy UI checks, or end-to-… |
| [`test-driven-development`](skills/test-driven-development/SKILL.md) | experimental | Use when implementing any feature or bug fix, before writing implementation code. Agree the seams to test, write one failing test, watch it fail for the right reason, write the minimum code to pass, watch it pass, then… |
| [`test-strategy`](skills/test-strategy/SKILL.md) | experimental | Use when deciding how a project should be tested rather than writing one test: the test portfolio and coverage targets, linking requirements and risks to tests, API and contract tests, performance benchmarks, regression… |
| [`verification-before-completion`](skills/verification-before-completion/SKILL.md) | experimental | Use when about to claim work is complete, fixed or passing, and before committing, opening a pull request or reporting success. Requires running the verification commands fresh and reading their output, so every claim i… |

## Origem e manutenção

- Entrada editorial: [manifesto de `testing`](../../catalog/curation/domains/testing.yaml).
- Requisitos: [spec do domínio](../../docs/specs/testing/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/testing/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `browser-testing` | affaan-m/ECC, anthropics/skills, currents-dev/playwright-best-practices-skill, github/awesome-copilot, openai/skills |
| `test-driven-development` | affaan-m/ECC, mattpocock/skills, obra/superpowers |
| `test-strategy` | affaan-m/ECC, davila7/claude-code-templates, github/awesome-copilot, msitarzewski/agency-agents, wshobson/agents |
| `verification-before-completion` | affaan-m/ECC, msitarzewski/agency-agents, obra/superpowers |
