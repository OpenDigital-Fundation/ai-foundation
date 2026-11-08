"""Copy permission follows the licence nearest to each file, not only the collection's lock entry."""
from pathlib import Path

import pytest

from tools.curation.licences import check_copy, effective_licence

APACHE = "                                 Apache License\n                           Version 2.0, January 2004\n"
SA = "Attribution-ShareAlike 4.0 International\n"
LOCK = {"a/apache": {"license": "Apache-2.0"}, "o/mixed": {"license": "NOASSERTION"}, "m/mod": {"license": "Modified MIT"}}


def tree(tmp_path: Path) -> Path:
    s = tmp_path / "sources"
    (s / "a_apache/skills/open").mkdir(parents=True)
    (s / "a_apache/skills/open/SKILL.md").write_text("# Open\n")
    (s / "a_apache/skills/restricted/references").mkdir(parents=True)
    (s / "a_apache/skills/restricted/LICENSE").write_text(SA)
    (s / "a_apache/skills/restricted/references/x.md").write_text("# X\n")
    (s / "a_apache/skills/cites").mkdir(parents=True)
    (s / "a_apache/skills/cites/SKILL.md").write_text("# Guide\n\nReference material based on OWASP Cheat Sheet Series (CC BY-SA 4.0).\n")
    (s / "a_apache/skills/mentions").mkdir(parents=True)
    (s / "a_apache/skills/mentions/SKILL.md").write_text("# Imagery\n\nPhotos are CC0, CC BY or CC BY-SA; credit CC BY-SA photos in the footer.\n")
    (s / "o_mixed/skills/apache").mkdir(parents=True)
    (s / "o_mixed/skills/apache/LICENSE.txt").write_text(APACHE)
    (s / "o_mixed/skills/apache/SKILL.md").write_text("# A\n")
    (s / "o_mixed/skills/none").mkdir(parents=True)
    (s / "o_mixed/skills/none/SKILL.md").write_text("# N\n")
    (s / "m_mod/x").mkdir(parents=True)
    (s / "m_mod/x/LICENSE").write_text("Modified MIT License\n")
    (s / "m_mod/x/a.md").write_text("# a\n")
    return s


def test_local_licence_overrides_lock(tmp_path):
    s = tree(tmp_path)
    assert effective_licence(LOCK, s, "o/mixed", "skills/apache/SKILL.md") == "Apache-2.0"
    assert effective_licence(LOCK, s, "a/apache", "skills/restricted/references/x.md") == "CC-BY-SA-4.0"
    assert effective_licence(LOCK, s, "a/apache", "skills/open/SKILL.md") == "Apache-2.0"
    assert effective_licence(LOCK, s, "o/mixed", "skills/apache") == "Apache-2.0"


@pytest.mark.parametrize("src,path", [
    ("a/apache", "skills/restricted/references/x.md"),   # ShareAlike subfolder of an Apache collection
    ("a/apache", "skills/restricted"),
    ("o/mixed", "skills/none/SKILL.md"),                 # no licence anywhere
    ("a/apache", "skills/cites/SKILL.md"),               # file declares it derives from CC BY-SA text
    ("a/apache", "skills/cites"),
])
def test_restricted_copies_are_refused(tmp_path, src, path):
    with pytest.raises(ValueError, match="does not permit copying"):
        check_copy(LOCK, tree(tmp_path), src, path)


def test_permissive_and_accepted_copies_pass(tmp_path):
    s = tree(tmp_path)
    assert check_copy(LOCK, s, "o/mixed", "skills/apache/SKILL.md") == "Apache-2.0"
    assert check_copy(LOCK, s, "a/apache", "skills/open") == "Apache-2.0"
    # describing third-party licences is not a declaration that the text itself derives from them
    assert check_copy(LOCK, s, "a/apache", "skills/mentions/SKILL.md") == "Apache-2.0"
    # a restricted licence the maintainer accepted in the lock (vendored with its licence text)
    assert check_copy(LOCK, s, "m/mod", "x/a.md").startswith("Restricted (Modified MIT)")
