# C# and F# on .NET — Tooling

Part of `languages:dotnet`. Load when formatters, linters, type checkers and editor hooks.

## C# Hooks

<!-- source: affaan-m/ECC rules/csharp/hooks.md -->

> This file extends [common/hooks.md](../common/hooks.md) with C#-specific content.

### PostToolUse Hooks

Configure in `~/.claude/settings.json`:

- **dotnet format**: Auto-format edited C# files and apply analyzer fixes
- **dotnet build**: Verify the solution or project still compiles after edits
- **dotnet test --no-build**: Re-run the nearest relevant test project after behavior changes

### Stop Hooks

- Run a final `dotnet build` before ending a session with broad C# changes
- Warn on modified `appsettings*.json` files so secrets do not get committed

## F# Hooks

<!-- source: affaan-m/ECC rules/fsharp/hooks.md -->

> This file extends [common/hooks.md](../common/hooks.md) with F#-specific content.

### PostToolUse Hooks

Configure in `~/.claude/settings.json`:

- **fantomas**: Auto-format edited F# files
- **dotnet build**: Verify the solution or project still compiles after edits
- **dotnet test --no-build**: Re-run the nearest relevant test project after behavior changes

### Stop Hooks

- Run a final `dotnet build` before ending a session with broad F# changes
- Warn on modified `appsettings*.json` files so secrets do not get committed
