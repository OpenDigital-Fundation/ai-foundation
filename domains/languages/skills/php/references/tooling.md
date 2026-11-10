# PHP — Tooling

Part of `languages:php`. Load when formatters, linters, type checkers and editor hooks.

## PHP Hooks

<!-- source: affaan-m/ECC rules/php/hooks.md -->

> This file extends common/hooks.md with PHP specific content.

### PostToolUse Hooks

Configure in `~/.claude/settings.json`:

- **Pint / PHP-CS-Fixer**: Auto-format edited `.php` files.
- **PHPStan / Psalm**: Run static analysis after PHP edits in typed codebases.
- **PHPUnit / Pest**: Run targeted tests for touched files or modules when edits affect behavior.

### Warnings

- Warn on `var_dump`, `dd`, `dump`, or `die()` left in edited files.
- Warn when edited PHP files add raw SQL or disable CSRF/session protections.
