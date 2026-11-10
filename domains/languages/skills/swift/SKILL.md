---
name: swift
description: "Use when writing, testing, reviewing or building Swift for iOS, macOS or visionOS - SwiftUI, Swift 6 strict concurrency and actors, persistence, protocol-based dependency injection, on-device Foundation Models and the Liquid Glass design language. Loads Swift Testing and XCTest usage, a review checklist and Xcode/SwiftPM build fixes."
license: MIT
metadata:
  domain: languages
  status: experimental
---

# Swift

Language-specific knowledge for Swift. The procedures themselves live elsewhere and are not repeated here: test-first work in `testing:test-driven-development`, review in `code-quality:code-review`, failures in `debugging:systematic-debugging`, security in `security:security-audit`. This pack adds what is specific to the language.

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

- [`swiftui`](references/frameworks/swiftui.md)
- [`liquid-glass`](references/frameworks/liquid-glass.md)
- [`foundation-models`](references/frameworks/foundation-models.md)

## Precedence

The repository's own standards, linters and `AGENTS.md` override anything in these references. When a reference contradicts the code base's established style, follow the code base and mention the difference.
