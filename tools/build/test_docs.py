import re
from pathlib import Path

from tools.build.docs import _load, _vocab, catalog_md, domain_readme, facets_md, sources_md
from tools.validate.repo import discover

import yaml

REPO = Path(__file__).resolve().parents[2]


def outputs():
    cat, exc, domains, lock, inv, arts, prov = _load(REPO)
    vocab = _vocab(REPO)
    facets = yaml.safe_load((REPO / "catalog/facets.yaml").read_text())["artifacts"]
    result = {
        REPO / "docs/CATALOG.md": catalog_md(REPO, cat, domains, arts),
        REPO / "docs/FACETS.md": facets_md(REPO, cat, vocab, facets),
        REPO / "docs/SOURCES.md": sources_md(REPO, cat, exc, lock, inv, prov),
    }
    result.update({REPO / "domains" / d / "README.md": domain_readme(REPO, d, boundary, cat, arts, prov, facets, vocab)
                   for d, boundary in domains.items()})
    return result


def test_generated_docs_are_current_and_deterministic():
    first = outputs()
    assert first == outputs()
    for path, text in first.items():
        assert path.read_text() == text, path


def test_every_artifact_is_linked_from_its_domain_and_the_catalog():
    catalog = (REPO / "docs/CATALOG.md").read_text()
    for artifact in discover(REPO):
        assert f"](../{artifact.path.relative_to(REPO).as_posix()})" in catalog
        readme = REPO / "domains" / artifact.domain / "README.md"
        assert f"]({artifact.path.relative_to(readme.parent).as_posix()})" in readme.read_text()


def test_documentation_links_point_to_existing_local_paths():
    paths = list(outputs()) + [REPO / "README.md", REPO / "AGENTS.md", REPO / "docs/README.md"]
    paths += list((REPO / "docs/architecture").glob("*.md"))
    paths += list((REPO / "docs/reviews").glob("*.md"))
    paths += list((REPO / "docs/specs").rglob("*.md"))
    for path in paths:
        text = re.sub(r"(?ms)^(```|~~~).*?^\1", "", path.read_text())
        for link in re.findall(r"\]\((?!https?://|#|mailto:)([^)\s]+)\)", text):
            target = link.split("#")[0]
            assert not target or (path.parent / target).resolve().exists(), (path, link)
