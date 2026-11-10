import shutil
from pathlib import Path

import pytest
import yaml

from tools.catalog import apply, rebuild
from tools.curation.manifests import load

REPO = Path(__file__).resolve().parents[2]


@pytest.fixture
def editorial(tmp_path):
    shutil.copytree(REPO / "catalog", tmp_path / "catalog")
    return tmp_path


def test_rebuild_preserves_public_registry_and_is_deterministic(editorial):
    paths = [editorial / "catalog" / f for f in ("catalog.yaml", "exclusions.yaml")]
    expected = [yaml.safe_load(p.read_text()) for p in paths]
    rebuild(editorial)
    assert [yaml.safe_load(p.read_text()) for p in paths] == expected
    first = [p.read_bytes() for p in paths]
    rebuild(editorial)
    assert [p.read_bytes() for p in paths] == first


@pytest.mark.parametrize("change, message", [
    (lambda d: d.update(domain="ui"), "domain must equal"),
    (lambda d: d["artifacts"].append(d["artifacts"][0].copy()), "duplicate artifact"),
    (lambda d: d["artifacts"][0].update(id="ui/foreign"), "another domain"),
    (lambda d: d["artifacts"][0].update(recipe={"description": "Synthetic recipe for testing", "body": "a"}, language_pack={"title": "x", "description": "Synthetic language pack", "topics": {}}), "cannot have both"),
    (lambda d: d["artifacts"][0].update(status="invalid"), "is not one of"),
    (lambda d: d.update(imports=[{"dest": "domains/testing/../../outside", "source": "x/y", "src": "x"}]), "destination must stay"),
])
def test_invalid_manifest_leaves_both_projections_untouched(editorial, change, message):
    outputs = [editorial / "catalog" / f for f in ("catalog.yaml", "exclusions.yaml")]
    before = [p.read_bytes() for p in outputs]
    path = editorial / "catalog/curation/domains/testing.yaml"
    data = yaml.safe_load(path.read_text())
    change(data)
    path.write_text(yaml.safe_dump(data))
    with pytest.raises(ValueError, match=message):
        rebuild(editorial)
    assert [p.read_bytes() for p in outputs] == before


def test_every_domain_has_one_editorial_owner(editorial):
    domains = yaml.safe_load((editorial / "catalog/domains.yaml").read_text())["domains"]
    assert set(load(editorial)) == set(domains)
    (editorial / "catalog/curation/domains/testing.yaml").rename(editorial / "catalog/curation/domains/unknown.yaml")
    with pytest.raises(ValueError, match="missing.*testing.*unknown"):
        load(editorial)


def test_apply_rejects_invalid_changes_without_mutating_editorial_inputs(editorial):
    paths = list((editorial / "catalog").rglob("*.yaml"))
    before = {p: p.read_bytes() for p in paths}
    with pytest.raises(ValueError):
        apply(editorial, {"artifacts": [{"id": "testing/test-strategy", "status": "invalid"}]})
    assert {p: p.read_bytes() for p in paths} == before


def test_invalid_exclusions_do_not_truncate_a_valid_registry(editorial):
    path = editorial / "catalog/curation/exclusions.yaml"
    path.write_text("version: 1\nexcluded: [{key: invalid}]\n")
    before = (editorial / "catalog/catalog.yaml").read_bytes()
    with pytest.raises(ValueError):
        rebuild(editorial)
    assert (editorial / "catalog/catalog.yaml").read_bytes() == before


def test_source_item_cannot_be_incorporated_and_excluded_at_once(editorial):
    manifest = yaml.safe_load((editorial / "catalog/curation/domains/testing.yaml").read_text())
    key = next(key for artifact in manifest["artifacts"] for key in artifact.get("supersedes", []))
    path = editorial / "catalog/curation/exclusions.yaml"
    data = yaml.safe_load(path.read_text())
    data["excluded"].append({"key": key, "reason": "out-of-scope"})
    path.write_text(yaml.safe_dump(data))
    before = (editorial / "catalog/catalog.yaml").read_bytes()
    with pytest.raises(ValueError, match="decided more than once"):
        rebuild(editorial)
    assert (editorial / "catalog/catalog.yaml").read_bytes() == before
