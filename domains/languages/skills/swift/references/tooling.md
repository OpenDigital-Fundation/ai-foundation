# Swift — Tooling

Part of `languages:swift`. Load when formatters, linters, type checkers and editor hooks.

## Swift Hooks

<!-- source: affaan-m/ECC rules/swift/hooks.md -->

> This file extends common/hooks.md with Swift specific content.

### PostToolUse Hooks

Configure in `~/.claude/settings.json`:

- **SwiftFormat**: Auto-format `.swift` files after edit
- **SwiftLint**: Run lint checks after editing `.swift` files
- **swift build**: Type-check modified packages after edit

### Warning

Flag `print()` statements — use `os.Logger` or structured logging instead for production code.
