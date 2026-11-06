# Rust — Tooling

Part of `languages:rust`. Load when formatters, linters, type checkers and editor hooks.

## Rust Hooks

<!-- source: affaan-m/ECC rules/rust/hooks.md -->

> This file extends [common/hooks.md](../common/hooks.md) with Rust-specific content.

### PostToolUse Hooks

Configure in `~/.claude/settings.json`:

- **cargo fmt**: Auto-format `.rs` files after edit
- **cargo clippy**: Run lint checks after editing Rust files
- **cargo check**: Verify compilation after changes (faster than `cargo build`)
