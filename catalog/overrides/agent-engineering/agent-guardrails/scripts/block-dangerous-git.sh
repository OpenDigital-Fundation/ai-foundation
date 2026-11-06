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
set +e
python3 -I -c '
import json, os, re, shlex, subprocess, sys

WRAPPERS = {"sudo", "env", "command", "nohup", "time", "exec", "builtin", "doas"}
GIT_OPTS_WITH_VALUE = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path", "--config-env"}
SEPARATORS = {";", "&&", "||", "|", "&", "\n", "(", ")", "|&"}
BUILTINS = {"push", "reset", "clean", "branch", "checkout", "restore", "commit", "status", "log", "diff", "add", "fetch",
            "pull", "merge", "rebase", "switch", "stash", "tag", "show", "remote", "config", "init", "clone", "rm", "mv",
            "worktree", "submodule", "cherry-pick", "revert", "blame", "grep", "bisect", "describe", "rev-parse", "ls-files"}
SAFE_CONFIG = re.compile(r"(color\.[a-z.]+|user\.(name|email)|core\.quotepath|log\.showsignature|init\.defaultbranch)=")
# Constructs the structured parser only partly understands; when present, also match the raw text.
INDIRECTION = re.compile(r"\beval\b|\bxargs\b|-exec(dir)?\b|\$\(|`|<\(|\bsource\b|\balias\b|\bfunction\b|\(\)\s*\{")
RAW_DANGER = re.compile(r"\bpush\b|reset\s+--hard|\bclean\s+-\S*f|branch\s+-D|--no-verify|\brm\s+-\S*(rf|fr)|checkout\s+\.(\s|$)|restore\s+\.(\s|$)")

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
    seg, prev, last = [], None, None
    for t in tokens + [";"]:
        if t in SEPARATORS or t == "`":
            if seg:
                yield seg, prev
            seg, prev = [], t
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

def check(seg, depth, piped=False):
    # Config injected through the environment changes what git runs: allow none of it.
    if any(re.match(r"GIT_CONFIG(_|=)|GIT_CONFIG_PARAMETERS=|GIT_EXEC_PATH=|GIT_SSH(_COMMAND)?=", a) for a in seg):
        block("git configuration injected through environment variables")
    if any(os.path.basename(a) == "env" for a in seg[:3]) and any(a == "-S" or a.startswith(("-S", "--split-string")) for a in seg):
        block("env -S builds a command line the guardrail cannot inspect")
    seg = strip_prefix(seg)
    if not seg:
        return
    prog = os.path.basename(seg[0])
    args = seg[1:]
    def recurse(text):
        for inner, sep in segments(text, depth + 1):
            check(inner, depth + 1, sep in {"|", "|&"})
    if prog in {"bash", "sh", "zsh", "dash", "ksh", "fish"}:
        for j, a in enumerate(args):
            if a.startswith("-") and not a.startswith("--") and "c" in a[1:]:
                if j + 1 < len(args):
                    recurse(args[j + 1])
                return
        scripts = [a for a in args if not a.startswith("-") and a not in {"<<<", "<<"}]
        if piped or "<<<" in args or "<<" in args or "-s" in args or not scripts:
            block(f"{prog} reading commands from stdin cannot be inspected")
        return  # known limit: a script file passed to a shell is not inspected
    if prog == "eval":
        recurse(" ".join(args))
        return
    if prog == "xargs":
        j = 0
        while j < len(args) and args[j].startswith("-"):
            j += 2 if args[j] in {"-I", "-L", "-n", "-P", "-s", "-d", "-E", "-a"} else 1
        if j < len(args):
            inner = os.path.basename(args[j])
            if inner in {"git", "bash", "sh", "zsh", "dash", "ksh", "fish", "env", "eval", "rm"}:
                block(f"xargs {inner} builds its arguments from data the guardrail cannot see")
            check(args[j:], depth + 1)
        return
    if prog == "find":
        for j, a in enumerate(args):
            if a in {"-exec", "-execdir", "-ok", "-okdir"}:
                end = next((k for k in range(j + 1, len(args)) if args[k] in {";", "+", "\\;"}), len(args))
                check(args[j + 1:end], depth + 1)
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
        value = args[i].split("=", 1)[1] if "=" in args[i] else (args[i + 1] if i + 1 < len(args) else "")
        if opt in {"-c", "--config-env"} and not SAFE_CONFIG.match(value.lower()):
            block(f"git {opt} {value.split("=")[0]} can change what git runs; only presentation settings are allowed")
        i += 2 if (opt in GIT_OPTS_WITH_VALUE and "=" not in args[i]) else 1
    if i >= len(args):
        return
    sub, rest = args[i], args[i + 1:]
    if sub not in BUILTINS:
        block(f"git {sub} is not a known git command (aliases are not inspected)")
    if "--no-verify" in rest or (sub == "commit" and "-n" in rest):
        block(f"git {sub} --no-verify skips the repository hooks")
    if sub == "config" and any(a.lower().startswith(("alias.", "include", "core.hookspath", "core.fsmonitor", "core.sshcommand", "core.pager", "core.editor", "core.gitproxy", "credential.")) for a in rest):
        block("git config would change what later git commands run")
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

if INDIRECTION.search(str(command)) and RAW_DANGER.search(str(command)):
    block("the command uses indirection the guardrail cannot fully inspect and mentions a destructive operation")
for s, sep in segments(str(command)):
    check(s, 0, sep in {"|", "|&"})
sys.exit(0)
'
status=$?
# Only 0 (allow) and 2 (block) are deliberate; any crash in the checker fails closed.
if [ "$status" -ne 0 ] && [ "$status" -ne 2 ]; then
  echo "BLOCKED: the git guardrail failed to inspect the command (status $status)." >&2
  exit 2
fi
exit "$status"
