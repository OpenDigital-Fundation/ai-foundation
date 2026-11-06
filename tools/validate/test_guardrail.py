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


@pytest.mark.parametrize("cmd", [
    "bash -lc 'git push'", "sh -ec \"git reset --hard\"", "eval git push", "eval 'git' 'push'",
    "echo origin | xargs git push", r"find . -name x -exec git push \;", "env -S 'git push'",
    "git -c alias.p=push p", "git -c core.hooksPath=/tmp/x commit -m x", "git --config-env=alias.p=X p",
    "f() { git push; }; f",
])
def test_blocks_indirection(cmd):
    assert run(cmd) == 2, cmd


def test_unknown_subcommand_blocked_even_if_alias(tmp_path):
    import subprocess as sp
    sp.run(["git", "init", "-q", str(tmp_path)], check=True)
    sp.run(["git", "-C", str(tmp_path), "config", "alias.ship", "push --force"], check=True)
    payload = json.dumps({"tool_input": {"command": "git ship"}})
    r = sp.run(["bash", str(SCRIPT)], input=payload, capture_output=True, text=True, cwd=tmp_path)
    assert r.returncode == 2


@pytest.mark.parametrize("cmd", [
    "env -S'git push'", "env --split-string='git push'", "FOO=1 env -S 'git status'",
    "echo push | xargs git", "echo 'git push' | bash", "bash <<< 'git push'", "cat script | sh -s",
    "git -c include.path=/tmp/x status", "git -c core.fsmonitor=evil status", "git -c core.gitProxy=x fetch",
    "GIT_CONFIG_PARAMETERS=\"'alias.st=push'\" git status", "GIT_CONFIG_COUNT=1 git status", "git st",
])
def test_blocks_config_and_stdin_shells(cmd):
    assert run(cmd) == 2, cmd


@pytest.mark.parametrize("cmd", ["git -c color.ui=always log", "bash scripts/test.sh", "sh ./run.sh --fast", "git -c user.name=x commit -m y"])
def test_allows_safe_forms(cmd):
    assert run(cmd) == 0, cmd


@pytest.mark.parametrize("cmd", ["git config alias.st push", "git config --global core.hooksPath /tmp/h", "git config include.path ../x"])
def test_blocks_dangerous_config_writes(cmd):
    assert run(cmd) == 2, cmd


def test_allows_harmless_config():
    assert run("git config user.email dev@example.com") == 0


@pytest.mark.parametrize("cmd", [
    "bash < cmds.txt", "sh <<<'git push'", "bash <<EOF\ngit push\nEOF", "sudo FOO=1 env -S 'git push'",
    "nice env --split-string='git push'", "echo x | xargs sudo git push", "echo x | xargs env git push",
    "git config core.askpass /tmp/x", "git config diff.external /tmp/x", "git config --global gpg.program /tmp/x",
])
def test_blocks_round_three(cmd):
    assert run(cmd) == 2, cmd


@pytest.mark.parametrize("cmd", ["git config --get user.email", "git config --list", "git config color.ui auto"])
def test_allows_config_reads_and_presentation(cmd):
    assert run(cmd) == 0, cmd


@pytest.mark.parametrize("cmd", [
    "git config color.ui.x.alias.y push", "git config --file .git/config alias.x push", "git config --comment x alias.x push",
    "git config --rename-section alias foo", "git config --remove-section core", "git config --edit", "git config unset user.name",
    "git config set alias.x push", "git config user.name a b", "git -c color.ui.hooksPath=x status", "git config --blob HEAD:x core.pager",
])
def test_blocks_config_parser_escapes(cmd):
    assert run(cmd) == 2, cmd


@pytest.mark.parametrize("cmd", ["git config user.name", "git config --global user.email a@b.c", "git config get user.email",
                                 "git config set color.ui auto", "git config --show-origin --list"])
def test_allows_strict_config(cmd):
    assert run(cmd) == 0, cmd
