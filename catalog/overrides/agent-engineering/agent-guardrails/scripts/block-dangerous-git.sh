#!/usr/bin/env bash
# PreToolUse guardrail for Bash: blocks destructive git and rm commands.
# Fails closed: if the input cannot be parsed, the command is blocked.
# This is a best-effort tripwire, not a security boundary: pair it with permission deny rules
# or an OS sandbox when the risk matters.
set -euo pipefail
if ! command -v python3 >/dev/null 2>&1; then
  echo "BLOCKED: the git guardrail needs python3 to inspect commands; install it or remove the hook." >&2
  exit 2
fi
exec python3 -I -c '
import json, os, shlex, sys

WRAPPERS = {"sudo", "env", "command", "nohup", "time", "exec", "builtin", "doas"}
GIT_OPTS_WITH_VALUE = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path", "--config-env"}
SEPARATORS = {";", "&&", "||", "|", "&", "\n", "(", ")", "|&"}

def block(reason):
    print(f"BLOCKED: {reason}. The user has prevented you from doing this.", file=sys.stderr)
    sys.exit(2)

try:
    data = json.load(sys.stdin)
    command = (data.get("tool_input") or {}).get("command")
except Exception:
    block("could not parse the hook input")
if command is None or not str(command).strip():
    sys.exit(0)

def segments(cmd, depth=0):
    if depth > 3:
        block("command nesting is too deep to inspect")
    try:
        lex = shlex.shlex(cmd.replace("$(", " ( ").replace("`", " ` "), posix=True, punctuation_chars=";&|()")
        lex.whitespace_split = True
        tokens = list(lex)
    except ValueError:
        block("could not tokenize the command")
    seg = []
    for t in tokens + [";"]:
        if t in SEPARATORS or t == "`":
            if seg:
                yield seg
            seg = []
        else:
            seg.append(t)

def strip_prefix(seg):
    i = 0
    while i < len(seg) and ("=" in seg[i] and not seg[i].startswith("-") and seg[i].split("=", 1)[0].isidentifier()):
        i += 1
    while i < len(seg) and os.path.basename(seg[i]) in WRAPPERS:
        i += 1
        while i < len(seg) and (seg[i].startswith("-") or ("=" in seg[i] and seg[i].split("=", 1)[0].isidentifier())):
            i += 1
    return seg[i:]

def check(seg, depth):
    seg = strip_prefix(seg)
    if not seg:
        return
    prog = os.path.basename(seg[0])
    args = seg[1:]
    if prog in {"bash", "sh", "zsh", "dash"} and "-c" in args:
        idx = args.index("-c")
        if idx + 1 < len(args):
            for inner in segments(args[idx + 1], depth + 1):
                check(inner, depth + 1)
        return
    if prog == "rm":
        flags = "".join(a.lstrip("-") for a in args if a.startswith("-") and not a.startswith("--"))
        longs = {a for a in args if a.startswith("--")}
        recursive = "r" in flags or "R" in flags or "--recursive" in longs
        force = "f" in flags or "--force" in longs
        if recursive and force:
            block("rm with recursive force deletes without confirmation")
        return
    if prog != "git":
        return
    i = 0
    while i < len(args) and args[i].startswith("-"):
        opt = args[i].split("=", 1)[0]
        i += 2 if (opt in GIT_OPTS_WITH_VALUE and "=" not in args[i]) else 1
    if i >= len(args):
        return
    sub, rest = args[i], args[i + 1:]
    if "--no-verify" in rest or (sub == "commit" and "-n" in rest):
        block(f"git {sub} --no-verify skips the repository hooks")
    if sub == "push":
        block("git push publishes to a remote")
    if sub == "reset" and "--hard" in rest:
        block("git reset --hard discards local changes")
    if sub == "clean" and any((a.startswith("-") and not a.startswith("--") and "f" in a) or a == "--force" for a in rest):
        block("git clean --force deletes untracked files")
    if sub == "branch" and ("-D" in rest or ({"-d", "--delete"} & set(rest) and {"-f", "--force"} & set(rest))):
        block("git branch force-delete removes unmerged work")
    if sub in {"checkout", "restore"} and "." in rest:
        block(f"git {sub} . discards changes in the working tree")

for s in segments(str(command)):
    check(s, 0)
sys.exit(0)
'
