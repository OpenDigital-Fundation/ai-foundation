"""Observable internal-discovery behaviour, including the installed portable snapshot."""
import copy
import json
from pathlib import Path
import runpy
import subprocess
import sys

import pytest

from tools.build.search import INDEX, SKILL, build, check

ROOT = Path(__file__).resolve().parents[2]
ENGINE = runpy.run_path(str(ROOT / SKILL / "scripts/find.py"))


@pytest.fixture(scope="module")
def index():
    return build(ROOT)


@pytest.mark.parametrize("query,expected", [
    ("design instrucional", "education/instructional-design"),
    ("TAXONOMIA DE BLOOM", "education/instructional-design"),
    ("aprender", "education/learn"),
    ("ensinar", "education/teach"),
    ("avaliação da aprendizagem", "education/learning-assessment"),
    ("design jurídico", "legal-compliance/legal-design"),
    ("Session Lens", "agent-engineering/session-observability"),
    ("busca interna", "agent-engineering/skill-discovery"),
])
def test_real_discovery_requests(index, query, expected):
    results = ENGINE["search"](index, query)["results"]
    assert results[0]["id"] == expected
    assert results[0]["matched_fields"]


def test_exact_id_and_filters(index):
    result = ENGINE["search"](index, "legal-compliance:legal-design", domain="legal-compliance", kind="skill", limit=1)
    assert [a["id"] for a in result["results"]] == ["legal-compliance/legal-design"]
    assert result["returned"] == 1
    result = ENGINE["search"](index, "", domain="education", kind="skill", limit=2)
    assert result["searched"] == 4
    assert result["returned"] == 2
    assert result["total_matches"] == 4


def test_absent_result_never_turns_into_a_recommendation(index):
    result = ENGINE["search"](index, "unlistedzzzz")
    assert result["results"] == [] and result["total_matches"] == 0


@pytest.mark.parametrize("options", [{"limit": 0}, {"limit": 51}, {"domain": "unknown"}, {"kind": "unknown"}])
def test_invalid_filters_and_limits(index, options):
    with pytest.raises(ValueError):
        ENGINE["search"](index, "", **options)


def test_deprecated_requires_opt_in(index):
    changed = copy.deepcopy(index)
    changed["artifacts"] = [dict(changed["artifacts"][0], status="deprecated")]
    assert ENGINE["search"](changed, "")["results"] == []
    assert len(ENGINE["search"](changed, "", include_deprecated=True)["results"]) == 1


def test_index_is_current_and_deterministic(index):
    assert build(ROOT) == index
    assert json.loads((ROOT / INDEX).read_text()) == index
    assert check(ROOT) == []


def test_portable_command_works_outside_checkout_and_does_not_write(tmp_path):
    script = ROOT / SKILL / "scripts/find.py"
    result = subprocess.run([sys.executable, str(script), "design instrucional", "--json"], cwd=tmp_path,
                            text=True, capture_output=True, check=True)
    report = json.loads(result.stdout)
    assert report["results"][0]["id"] == "education/instructional-design"
    assert "installation was not checked" in report["availability"]
    assert list(tmp_path.iterdir()) == []


def test_repo_cli_uses_same_results(index):
    result = subprocess.run([sys.executable, "-m", "tools.catalog", "find", "Session Lens", "--json"],
                            cwd=ROOT, text=True, capture_output=True, check=True)
    assert json.loads(result.stdout) == ENGINE["search"](index, "Session Lens")


def test_stale_snapshot_and_unknown_term_owner_are_rejected(tmp_path):
    # Only declared catalog metadata and local package files are copied, never personal records.
    import shutil
    shutil.copytree(ROOT / "catalog", tmp_path / "catalog")
    shutil.copytree(ROOT / "domains", tmp_path / "domains")
    (tmp_path / INDEX).write_text('{}\n')
    assert "stale index" in check(tmp_path)[0]
    terms_path = tmp_path / SKILL / "assets/search-terms.json"
    terms = json.loads(terms_path.read_text());terms['unknown/missing']=['test'];terms_path.write_text(json.dumps(terms))
    with pytest.raises(ValueError, match="existing catalog IDs"):
        build(tmp_path)
