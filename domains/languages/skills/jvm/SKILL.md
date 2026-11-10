---
name: jvm
description: "Use when writing, testing, reviewing or building Java or Kotlin on the JVM or Android - Spring Boot, Quarkus, JPA/Hibernate, MyBatis, Exposed, Ktor, coroutines and Flow, Jetpack and Compose Multiplatform. Loads coding standards, JUnit 5, Mockito, MockK, Kotest and Testcontainers usage, Spring Security patterns, a review checklist and Maven/Gradle build fixes."
license: MIT
metadata:
  domain: languages
  status: experimental
---

# Java and Kotlin

Language-specific knowledge for Java and Kotlin. The procedures themselves live elsewhere and are not repeated here: test-first work in `testing:test-driven-development`, review in `code-quality:code-review`, failures in `debugging:systematic-debugging`, security in `security:security-audit`. This pack adds what is specific to the language.

## Load only what the task needs

| Reference | Load when |
|---|---|
| [`references/standards.md`](references/standards.md) | writing or refactoring code: style, idioms, patterns, project layout |
| [`references/testing.md`](references/testing.md) | writing or fixing tests: runner, fixtures, mocking, coverage |
| [`references/security.md`](references/security.md) | code that handles untrusted input, auth, secrets, files, network or SQL |
| [`references/review.md`](references/review.md) | reviewing a change; read by `code-quality:code-reviewer` |
| [`references/build.md`](references/build.md) | compiler, build tool, type-checker or dependency failures |
| [`references/tooling.md`](references/tooling.md) | formatters, linters, type checkers and editor hooks |

## Frameworks

Load the framework file only when the project uses it (check the manifest: `package.json`, `pyproject.toml`, `build.gradle`, `Gemfile`, `composer.json`, `pubspec.yaml`, `Package.swift`).

- [`spring-boot`](references/frameworks/spring-boot.md)
- [`quarkus`](references/frameworks/quarkus.md)
- [`jpa`](references/frameworks/jpa.md)
- [`mybatis`](references/frameworks/mybatis.md)
- [`exposed`](references/frameworks/exposed.md)
- [`ktor`](references/frameworks/ktor.md)
- [`android`](references/frameworks/android.md)
- [`compose-multiplatform`](references/frameworks/compose-multiplatform.md)

## Precedence

The repository's own standards, linters and `AGENTS.md` override anything in these references. When a reference contradicts the code base's established style, follow the code base and mention the difference.
