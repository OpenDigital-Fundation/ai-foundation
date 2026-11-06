"""Regression tests for the vendored (and hardened) git guardrail hook."""
import json
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "catalog/overrides/agent-engineering/agent-guardrails/scripts/block-dangerous-git.sh"


def run(command):
    payload = json.dumps({"tool_input": {"command": command}}) if command is not None else "not json"
    return subprocess.run(["bash", str(SCRIPT)], input=payload, capture_output=True, text=True).returncode


@pytest.mark.parametrize("cmd", [
    "git push", "git  push origin main", "git -C repo push", "git -c core.x=y push --force",
    "FOO=1 git push", "sudo git push", "echo ok && git push", "ls; git reset --hard HEAD~1",
    "git clean -fdx", "git clean --force", "git branch -D feature", "git branch --delete --force feature",
    "git checkout .", "git restore .", "git commit --no-verify -m x", "git commit -n -m x",
    "rm -rf build", "rm -fr /tmp/x", "rm -r -f dir", "rm --recursive --force dir",
    "bash -c 'git push'", "sh -c \"git reset --hard\"", "echo $(git push)", "git commit -m 'unbalanced",
])
def test_blocks(cmd):
    assert run(cmd) == 2, cmd


@pytest.mark.parametrize("cmd", [
    "git status", "git commit -m 'push the button'", "git log --oneline", "git branch -d merged",
    "git checkout feature", "git restore src/app.ts", "rm file.txt", "rm -r emptydir", "echo git push is blocked",
    "grep -r 'reset --hard' docs", "",
])
def test_allows(cmd):
    assert run(cmd) == 0, cmd


def test_invalid_input_fails_closed():
    assert run(None) == 2
