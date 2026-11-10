# `languages`

<!-- Gerado por `python -m tools.build docs` a partir de catalog/. Não editar. -->

Idiomatic knowledge per programming language and framework, one pack per language.

[Catálogo completo](../../docs/CATALOG.md) · [Facetas](../../docs/FACETS.md) · [Manutenção](../../docs/architecture/repository-layout.md)

## Instalação

```text
/plugin marketplace add OpenDigital-Fundation/ai-foundation
/plugin install languages@opendigital-ai-foundation
```

## Conteúdo

As descrições abaixo vêm dos artefatos e mantêm seu idioma original.

### knowledge

| Artefato | Estado | Quando usar |
|---|---|---|
| [`external-tools`](knowledge/external-tools.md) | experimental | External language tools referenced, not vendored: react-doctor (restricted licence), godoctor, Vercel interface guidelines. |

### skill

| Artefato | Estado | Quando usar |
|---|---|---|
| [`cpp`](skills/cpp/SKILL.md) | experimental | Use when writing, testing, reviewing or building C++ code. Loads modern C++ standards (RAII, ownership with smart pointers, const-correctness, the Core Guidelines), GoogleTest and CTest usage with sanitizers and coverag… |
| [`dart`](skills/dart/SKILL.md) | experimental | Use when writing, testing, reviewing or building Dart or Flutter apps. Loads widget composition and state management (BLoC, Riverpod, Provider), Dart idioms and null safety, widget, golden and integration tests, a Flutt… |
| [`dotnet`](skills/dotnet/SKILL.md) | experimental | Use when writing, testing, reviewing or building C# or F# on .NET - ASP.NET Core, Entity Framework, dependency injection, async/await. Loads .NET patterns, xUnit, FluentAssertions, FsUnit and FsCheck usage, .NET securit… |
| [`go`](skills/go/SKILL.md) | experimental | Use when writing, testing, reviewing or building Go code. Loads idiomatic Go (errors, interfaces, context, concurrency with goroutines and channels), table-driven tests, subtests, fuzzing and benchmarks, Go security pit… |
| [`jvm`](skills/jvm/SKILL.md) | experimental | Use when writing, testing, reviewing or building Java or Kotlin on the JVM or Android - Spring Boot, Quarkus, JPA/Hibernate, MyBatis, Exposed, Ktor, coroutines and Flow, Jetpack and Compose Multiplatform. Loads coding s… |
| [`php`](skills/php/SKILL.md) | experimental | Use when writing, testing, reviewing or building PHP, including Laravel applications. Loads PSR standards and modern PHP patterns, Eloquent and service-container usage, PHPUnit and Pest tests with factories, Laravel sec… |
| [`python`](skills/python/SKILL.md) | experimental | Use when writing, testing, reviewing or building Python - scripts, packages, Django, Django REST Framework, Celery, FastAPI or PyTorch code. Loads idiomatic patterns and typing, pytest fixtures and mocking, Django and F… |
| [`react-diagnostics`](skills/react-diagnostics/SKILL.md) | experimental | Use when finishing a feature, fixing a bug or before committing React code, or when the user types /doctor or asks to scan, triage or clean up React diagnostics. Runs React Doctor across lint, accessibility, performance… |
| [`ruby`](skills/ruby/SKILL.md) | experimental | Use when writing, testing, reviewing or building Ruby, including Ruby on Rails applications. Loads Ruby style and idioms, Rails conventions (ActiveRecord, service objects, background jobs), RSpec and Minitest usage, Rai… |
| [`rust`](skills/rust/SKILL.md) | experimental | Use when writing, testing, reviewing, refactoring or building Rust code. Loads ownership and borrowing patterns, error handling with Result and thiserror/anyhow, async with Tokio, unit, integration, property and async t… |
| [`swift`](skills/swift/SKILL.md) | experimental | Use when writing, testing, reviewing or building Swift for iOS, macOS or visionOS - SwiftUI, Swift 6 strict concurrency and actors, persistence, protocol-based dependency injection, on-device Foundation Models and the L… |
| [`typescript`](skills/typescript/SKILL.md) | experimental | Use when writing, testing, reviewing or building TypeScript or JavaScript - Node, Bun, browser code, or the React, React Native, Next.js, Vue, Nuxt, Angular, NestJS and Vite ecosystems. Loads idiomatic patterns, Vitest/… |

## Origem e manutenção

- Entrada editorial: [manifesto de `languages`](../../catalog/curation/domains/languages.yaml).
- Requisitos: [spec do domínio](../../docs/specs/languages/catalog/spec.md).
- Origem por arquivo: [PROVENANCE.yaml](PROVENANCE.yaml); licenças e decisões: [fontes](../../docs/SOURCES.md).
- Artefatos com receita são reconstruídos a partir do manifesto; ajustes em arquivos gerados ficam em `catalog/overrides/languages/<skill>/`. Consulte o guia antes de editar.

| Artefato | Fontes |
|---|---|
| `external-tools` | contribuição original |
| `cpp` | affaan-m/ECC, github/awesome-copilot |
| `dart` | affaan-m/ECC, github/awesome-copilot |
| `dotnet` | affaan-m/ECC, github/awesome-copilot |
| `go` | affaan-m/ECC, github/awesome-copilot |
| `jvm` | affaan-m/ECC, github/awesome-copilot |
| `php` | affaan-m/ECC, github/awesome-copilot |
| `python` | affaan-m/ECC, github/awesome-copilot |
| `react-diagnostics` | github/awesome-copilot, millionco/react-doctor |
| `ruby` | affaan-m/ECC, github/awesome-copilot |
| `rust` | affaan-m/ECC, github/awesome-copilot, msitarzewski/agency-agents |
| `swift` | affaan-m/ECC |
| `typescript` | affaan-m/ECC, github/awesome-copilot, mattpocock/skills, msitarzewski/agency-agents, vercel-labs/agent-skills |
