---
name: cpp
description: "Use when writing, testing, reviewing or building C++ code. Loads modern C++ standards (RAII, ownership with smart pointers, const-correctness, the Core Guidelines), GoogleTest and CTest usage with sanitizers and coverage, memory-safety pitfalls, a review checklist and fixes for CMake, compiler and linker errors."
license: MIT
metadata:
  domain: languages
  status: experimental
---

# C++

Language-specific knowledge for C++. The procedures themselves live elsewhere and are not repeated here: test-first work in `testing:test-driven-development`, review in `code-quality:code-review`, failures in `debugging:systematic-debugging`, security in `security:security-audit`. This pack adds what is specific to the language.

## Load only what the task needs

| Reference | Load when |
|---|---|
| [`references/standards.md`](references/standards.md) | writing or refactoring code: style, idioms, patterns, project layout |
| [`references/testing.md`](references/testing.md) | writing or fixing tests: runner, fixtures, mocking, coverage |
| [`references/security.md`](references/security.md) | code that handles untrusted input, auth, secrets, files, network or SQL |
| [`references/review.md`](references/review.md) | reviewing a change; read by `code-quality:code-reviewer` |
| [`references/build.md`](references/build.md) | compiler, build tool, type-checker or dependency failures |
| [`references/tooling.md`](references/tooling.md) | formatters, linters, type checkers and editor hooks |

## Precedence

The repository's own standards, linters and `AGENTS.md` override anything in these references. When a reference contradicts the code base's established style, follow the code base and mention the difference.
