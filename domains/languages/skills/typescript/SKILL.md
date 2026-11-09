---
name: typescript
description: "Use when writing, testing, reviewing or building TypeScript or JavaScript - Node, Bun, browser code, or the React, React Native, Next.js, Vue, Nuxt, Angular, NestJS and Vite ecosystems. Loads idiomatic patterns, Vitest/Jest and Testing Library usage, XSS and supply-chain pitfalls, a review checklist and fixes for tsc, bundler and build errors."
license: MIT
metadata:
  domain: languages
  status: experimental
---

# TypeScript and JavaScript

Language-specific knowledge for TypeScript and JavaScript. The procedures themselves live elsewhere and are not repeated here: test-first work in `testing:test-driven-development`, review in `code-quality:code-review`, failures in `debugging:systematic-debugging`, security in `security:security-audit`. This pack adds what is specific to the language.

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

- [`react`](references/frameworks/react.md)
- [`react-native`](references/frameworks/react-native.md)
- [`nextjs`](references/frameworks/nextjs.md)
- [`vue`](references/frameworks/vue.md)
- [`nuxt`](references/frameworks/nuxt.md)
- [`angular`](references/frameworks/angular.md)
- [`nestjs`](references/frameworks/nestjs.md)
- [`vite`](references/frameworks/vite.md)
- [`bun`](references/frameworks/bun.md)
- [`electron`](references/frameworks/electron.md)
- [`astro`](references/frameworks/astro.md)
- [`svelte`](references/frameworks/svelte.md)
- [`tanstack`](references/frameworks/tanstack.md)

## Precedence

The repository's own standards, linters and `AGENTS.md` override anything in these references. When a reference contradicts the code base's established style, follow the code base and mention the difference.
