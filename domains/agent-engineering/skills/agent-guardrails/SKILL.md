---
name: agent-guardrails
description: "Use when an agent should be prevented from destructive or risky actions: blocking dangerous git and shell commands (push, reset --hard, clean, rm -rf, --no-verify) with harness hooks, careful and frozen modes, and protecting configuration files. Hooks are opt-in and installed only with the user's approval."
license: MIT
metadata:
  domain: agent-engineering
  status: experimental
---
# Setup Git Guardrails

Sets up a PreToolUse hook that intercepts and blocks dangerous git commands before Claude executes them.

## What Gets Blocked

- `git push` (all variants including `--force`)
- `git reset --hard`
- `git clean -f` / `git clean -fd`
- `git branch -D`
- `git checkout .` / `git restore .`

When blocked, Claude sees a message telling it that it does not have authority to access these commands.

## Steps

### 1. Ask scope

Ask the user: install for **this project only** (`.claude/settings.json`) or **all projects** (`~/.claude/settings.json`)?

### 2. Copy the hook script

The bundled script is at: [scripts/block-dangerous-git.sh](scripts/block-dangerous-git.sh)

Copy it to the target location based on scope:

- **Project**: `.claude/hooks/block-dangerous-git.sh`
- **Global**: `~/.claude/hooks/block-dangerous-git.sh`

Make it executable with `chmod +x`.

### 3. Add hook to settings

Add to the appropriate settings file:

**Project** (`.claude/settings.json`):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

**Global** (`~/.claude/settings.json`):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

If the settings file already exists, merge the hook into the existing `hooks.PreToolUse` array. Don't overwrite other settings.

### 4. Ask about customization

Ask if user wants to add or remove any patterns from the blocked list. Edit the copied script accordingly.

### 5. Verify

Run a quick test:

```bash
echo '{"tool_input":{"command":"git push origin main"}}' | <path-to-script>
```

Should exit with code 2 and print a BLOCKED message to stderr.

## Limits of this guardrail

- The hook script is a best-effort tripwire, not a security boundary. It tokenises the command with `shlex`, follows `bash -c` and `$(...)`, skips git global options and environment prefixes, and **fails closed** (blocks) when it cannot parse the input. Determined obfuscation can still get past any pattern check: for real protection, add permission deny rules or run the agent in an OS sandbox.
- It needs `python3` on the machine; without it every Bash call is blocked with an explanation.
- Besides git (`push`, `reset --hard`, `clean -f`, `branch -D`, `checkout .`, `restore .`, `--no-verify`) it blocks `rm` with recursive force.
- Installing the hook changes the user's harness settings: show the exact file and JSON first and install only after explicit approval.

## References

Load only what the task needs:

- [`references/safety-modes.md`](references/safety-modes.md)
