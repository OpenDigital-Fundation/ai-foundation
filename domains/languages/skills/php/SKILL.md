---
name: php
description: "Use when writing, testing, reviewing or building PHP, including Laravel applications. Loads PSR standards and modern PHP patterns, Eloquent and service-container usage, PHPUnit and Pest tests with factories, Laravel security (CSRF, mass assignment, authorization) and a verification loop with static analysis."
license: MIT
metadata:
  domain: languages
  status: experimental
---

# PHP

Language-specific knowledge for PHP. The procedures themselves live elsewhere and are not repeated here: test-first work in `testing:test-driven-development`, review in `code-quality:code-review`, failures in `debugging:systematic-debugging`, security in `security:security-audit`. This pack adds what is specific to the language.

## Load only what the task needs

| Reference | Load when |
|---|---|
| [`references/standards.md`](references/standards.md) | writing or refactoring code: style, idioms, patterns, project layout |
| [`references/testing.md`](references/testing.md) | writing or fixing tests: runner, fixtures, mocking, coverage |
| [`references/security.md`](references/security.md) | code that handles untrusted input, auth, secrets, files, network or SQL |
| [`references/review.md`](references/review.md) | reviewing a change; read by `code-quality:code-reviewer` |
| [`references/tooling.md`](references/tooling.md) | formatters, linters, type checkers and editor hooks |

## Frameworks

Load the framework file only when the project uses it (check the manifest: `package.json`, `pyproject.toml`, `build.gradle`, `Gemfile`, `composer.json`, `pubspec.yaml`, `Package.swift`).

- [`laravel`](references/frameworks/laravel.md)

## Precedence

The repository's own standards, linters and `AGENTS.md` override anything in these references. When a reference contradicts the code base's established style, follow the code base and mention the difference.
