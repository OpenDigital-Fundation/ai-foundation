# Spec — Catálogo do domínio `languages`

- **Domínio:** languages
- **Status:** em implementação (Onda 2)
- **ADR:** [language-packs](../../../adr/foundation/language-packs.md)
- **Fronteira:** conhecimento idiomático por linguagem e framework, um pacote por linguagem.

## Problema

O ECC tem, por linguagem, rules (`coding-style`, `patterns`, `security`, `testing`, `hooks`), skills `*-patterns`/`*-testing`/`*-tdd`/`*-security`/`*-verification`, agents `*-reviewer`/`*-build-resolver` e comandos `*-review`/`*-test`/`*-build`: 209 itens que repetem os mesmos procedimentos genéricos com detalhes da linguagem.

## Resultado

Onze pacotes (`typescript`, `python`, `go`, `rust`, `jvm`, `swift`, `dart`, `dotnet`, `cpp`, `php`, `ruby`). Cada um é uma skill com `SKILL.md` curto (índice) e referências carregadas sob demanda:

| Arquivo | Origem típica |
|---|---|
| `references/standards.md` | rules `coding-style` e `patterns`, skill `*-patterns` |
| `references/testing.md` | rule `testing`, skills `*-testing` |
| `references/security.md` | rule `security` |
| `references/review.md` | agent `*-reviewer` (lido pelo `code-quality:code-reviewer`) |
| `references/build.md` | agent `*-build-resolver` (lido no debugging de erros de build) |
| `references/tooling.md` | rule `hooks` |
| `references/frameworks/<fw>.md` | skills e agents de framework (Django, FastAPI, React, Vue, Spring Boot, Quarkus, Laravel, Rails, SwiftUI...) |

## Como é gerado

`python -m tools.curation.language_pack <sources> catalog/decisions/language-packs.yaml` monta os pacotes a partir do mapa declarativo, gera a proveniência de cada arquivo (várias fontes por arquivo) e o `catalog/decisions/languages.yaml`. O conteúdo de `domains/languages/skills/` é **saída gerada**: para mudar, edite o mapa e regenere. O montador reescreve referências internas do upstream (`python-patterns`, `/go-review`) para os artefatos deste catálogo.

## Pendências

- Referências a itens ainda sem casa no catálogo: `backend-patterns`, `coding-standards`, `docker-patterns`, `e2e-testing`, `mysql-patterns`, `postgres-patterns`, `prisma-patterns`, `typescript-build-resolver`. Resolvem-se com os domínios `data`, `platform` e `testing` (browser).
- Revisão humana do conteúdo: o texto vem do ECC com edição mecânica; regras absolutas que contrariem `principles:coding-discipline` devem ser podadas pacote a pacote.
- Fora de escopo v1: Perl, ArkTS/HarmonyOS.
