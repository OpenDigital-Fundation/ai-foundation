import json
import sys
from pathlib import Path

from tools.evals.triggers import Case, first_skill, run_case


def _event(skill: str) -> str:
    return json.dumps({"type": "assistant", "message": {"content": [
        {"type": "text", "text": "ok"},
        {"type": "tool_use", "name": "Skill", "input": {"skill": skill}}]}})


def test_first_skill_parses_stream_json():
    lines = ['{"type":"system"}', "not json", _event("testing:test-driven-development"), _event("other:x")]
    assert first_skill(lines) == "testing:test-driven-development"
    assert first_skill(['{"type":"result"}']) is None


def fake_harness(tmp_path: Path, mapping: dict[str, str]) -> list[str]:
    script = tmp_path / "fake.py"
    script.write_text(
        "import json, sys\n"
        f"m = {mapping!r}\n"
        "p = sys.argv[-1]\n"
        "s = next((v for k, v in m.items() if k in p), None)\n"
        "print(json.dumps({'type': 'system'}))\n"
        "if s: print(json.dumps({'type': 'assistant', 'message': {'content': [{'type': 'tool_use', 'name': 'Skill', 'input': {'skill': s}}]}}))\n"
        "print(json.dumps({'type': 'result'}))\n")
    return [sys.executable, str(script)]


def test_should_trigger_and_should_not(tmp_path):
    cmd = fake_harness(tmp_path, {"slugify": "testing:test-driven-development", "flaky": "debugging:systematic-debugging"})
    t = "testing:test-driven-development"
    assert run_case(cmd, Case("implement slugify", t, t, "should_trigger")).passed
    assert not run_case(cmd, Case("why is it flaky", t, t, "should_trigger")).passed
    assert run_case(cmd, Case("why is it flaky", None, t, "should_not_trigger")).passed
    assert not run_case(cmd, Case("implement slugify", None, t, "should_not_trigger")).passed


def test_routing_expect_none(tmp_path):
    cmd = fake_harness(tmp_path, {})
    assert run_case(cmd, Case("hello", None, "routing", "routing")).passed


def test_api_error_is_reported_not_scored(tmp_path):
    script = tmp_path / "err.py"
    script.write_text("import json\nprint(json.dumps({'type': 'result', 'terminal_reason': 'api_error'}, separators=(',', ':')))\n")
    r = run_case([sys.executable, str(script)], Case("x", None, "t:x", "should_not_trigger"))
    assert not r.passed and r.error
