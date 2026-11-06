---
name: python
description: "Use when writing, testing, reviewing or building Python - scripts, packages, Django, Django REST Framework, Celery, FastAPI or PyTorch code. Loads idiomatic patterns and typing, pytest fixtures and mocking, Django and FastAPI security, a review checklist, packaging and verification loops (ruff, mypy, pip-audit, bandit)."
license: MIT
metadata:
  domain: languages
  status: experimental
---

# Python

Language-specific knowledge for Python. The procedures themselves live elsewhere and are not repeated here: test-first work in `testing:test-driven-development`, review in `code-quality:code-review`, failures in `debugging:systematic-debugging`, security in `security:security-audit`. This pack adds what is specific to the language.

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

- [`django`](references/frameworks/django.md)
- [`fastapi`](references/frameworks/fastapi.md)
- [`pytorch`](references/frameworks/pytorch.md)

## Precedence

The repository's own standards, linters and `AGENTS.md` override anything in these references. When a reference contradicts the code base's established style, follow the code base and mention the difference.
