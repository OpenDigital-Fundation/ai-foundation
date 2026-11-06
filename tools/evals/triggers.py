"""Trigger and routing evals: does the right skill fire for a prompt, and only that one?

  python -m tools.evals.triggers [--skill <domain/name> ...] [--routing] [--jobs N]

Sources of cases:
  domains/<d>/skills/<s>/evals/triggers.yaml   should_trigger / should_not_trigger lists
  evals/routing/*.yaml                         [{prompt, expect: <domain:skill> | none}]

The harness is a command that receives the prompt as its last argument and prints Claude Code
stream-json on stdout. Default: Claude Code in bare print mode with every domain plugin loaded,
plan permission mode, in an empty temporary directory. Override with FOUNDATION_EVAL_HARNESS
(a shell-style command line). Each run stops at the first Skill invocation.
Running the default harness calls the model and is billed.
"""
from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from pathlib import Path

import yaml

TIMEOUT_S = 180


@dataclass
class Case:
    prompt: str
    expect: str | None        # "<domain>:<skill>" that must fire, or None for "must not fire <target>"
    target: str               # the skill under test ("<domain>:<skill>"), or "routing"
    kind: str                 # should_trigger | should_not_trigger | routing


@dataclass
class Result:
    case: Case
    fired: str | None
    passed: bool
    seconds: float
    error: str | None = None


def default_harness(root: Path) -> list[str]:
    cmd = ["claude", "--bare", "-p", "--output-format", "stream-json", "--verbose", "--permission-mode", "plan"]
    for d in sorted((root / "domains").iterdir()):
        if (d / ".claude-plugin/plugin.json").is_file():
            cmd += ["--plugin-dir", str(d)]
    return cmd


def harness(root: Path) -> list[str]:
    env = os.environ.get("FOUNDATION_EVAL_HARNESS")
    if env:
        return shlex.split(env)
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is required: the default harness runs Claude Code in --bare mode, "
                 "which never reads OAuth or keychain credentials. Runs are billed.")
    return default_harness(root)


def _api_error(line: str) -> str | None:
    if '"terminal_reason":"api_error"' in line.replace(" ", "") or "Not logged in" in line:
        return "harness reported an API/authentication error"
    return None


def first_skill(lines) -> str | None:
    """Return the skill named by the first Skill tool_use event in a stream-json transcript."""
    for line in lines:
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        content = (ev.get("message") or {}).get("content") or []
        for block in content if isinstance(content, list) else []:
            if isinstance(block, dict) and block.get("type") == "tool_use" and block.get("name") == "Skill":
                return str((block.get("input") or {}).get("skill") or (block.get("input") or {}).get("command") or "")
    return None


def _normalise(name: str | None) -> str | None:
    if not name:
        return None
    name = name.lstrip("/")
    return name


def run_case(cmd: list[str], case: Case) -> Result:
    start = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="foundation-eval-") as cwd:
        # An empty config dir keeps the user's own installed plugins and memory out of the run.
        env = {**os.environ, "CLAUDE_CONFIG_DIR": str(Path(cwd) / ".config")}
        try:
            proc = subprocess.Popen(cmd + [case.prompt], cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        except OSError as e:
            return Result(case, None, False, 0.0, f"harness failed to start: {e}")
        fired, error = None, None
        try:
            for line in proc.stdout:
                error = error or _api_error(line)
                fired = first_skill([line])
                if fired or time.monotonic() - start > TIMEOUT_S:
                    break
        finally:
            proc.kill()
            proc.wait()
    fired = _normalise(fired)
    if error and not fired:
        return Result(case, None, False, round(time.monotonic() - start, 1), error)
    if case.kind == "should_not_trigger":
        passed = fired != case.target
    else:
        passed = fired == case.expect
    return Result(case, fired, passed, round(time.monotonic() - start, 1))


def collect(root: Path, skills: list[str] | None, routing: bool) -> list[Case]:
    cases: list[Case] = []
    for f in sorted((root / "domains").glob("*/skills/*/evals/triggers.yaml")) + sorted((root / "domains").glob("*/workflows/*/evals/triggers.yaml")):
        domain, name = f.parts[-5], f.parts[-3]
        if skills and f"{domain}/{name}" not in skills:
            continue
        target = f"{domain}:{name}"
        data = yaml.safe_load(f.read_text()) or {}
        cases += [Case(p, target, target, "should_trigger") for p in data.get("should_trigger") or []]
        cases += [Case(p, None, target, "should_not_trigger") for p in data.get("should_not_trigger") or []]
    if routing:
        for f in sorted((root / "evals/routing").glob("*.yaml")):
            for c in yaml.safe_load(f.read_text()) or []:
                exp = None if c["expect"] in (None, "none") else c["expect"]
                cases.append(Case(c["prompt"], exp, "routing", "routing"))
    return cases


def summarise(results: list[Result]) -> dict:
    by_target: dict[str, dict] = {}
    for r in results:
        t = by_target.setdefault(r.case.target, {"passed": 0, "total": 0, "failures": []})
        t["total"] += 1
        if r.passed:
            t["passed"] += 1
        else:
            t["failures"].append({"prompt": r.case.prompt, "kind": r.case.kind, "expected": r.case.expect, "fired": r.fired, "error": r.error})
    return by_target


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill", action="append", help="domain/name; repeatable; default all with evals")
    ap.add_argument("--routing", action="store_true", help="include evals/routing cases")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--out", default="evals/results/triggers.json")
    args = ap.parse_args(argv)
    root = Path(".").resolve()
    cases = collect(root, args.skill, args.routing)
    if not cases:
        print("no cases found")
        return 1
    cmd = harness(root)
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(lambda c: run_case(cmd, c), cases))
    summary = summarise(results)
    out = root / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"summary": summary, "results": [asdict(r) for r in results]}, indent=2))
    failed = 0
    for target, s in sorted(summary.items()):
        print(f"{target:55} {s['passed']}/{s['total']}")
        for f in s["failures"]:
            failed += 1
            print(f"   FAIL [{f['kind']}] expected={f['expected']} fired={f['fired']} :: {f['prompt'][:80]}")
    print(f"{len(results) - failed}/{len(results)} passed -> {out.relative_to(root)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
