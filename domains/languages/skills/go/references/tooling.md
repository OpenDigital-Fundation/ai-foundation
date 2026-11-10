# Go — Tooling

Part of `languages:go`. Load when formatters, linters, type checkers and editor hooks.

## Go Hooks

<!-- source: affaan-m/ECC rules/golang/hooks.md -->

> This file extends common/hooks.md with Go specific content.

### PostToolUse Hooks

Configure in `~/.claude/settings.json`:

- **gofmt/goimports**: Auto-format `.go` files after edit
- **go vet**: Run static analysis after editing `.go` files
- **staticcheck**: Run extended static checks on modified packages
