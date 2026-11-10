from tools.inventory.sync_report import safe


def test_safe_keeps_normal_names():
    assert safe("affaan-m/ECC:skill:tdd-workflow") == "`affaan-m/ECC:skill:tdd-workflow`"
    assert safe("msitarzewski/agency-agents:agent:Payments & Billing Engineer").startswith("`msitarzewski")


def test_safe_neutralises_markdown_and_mentions():
    assert "@" not in safe("someone/repo:skill:@octocat")
    for evil in ["x` [click](https://evil) `", "a\nb", "<img src=x onerror=alert(1)>", "x|y"]:
        out = safe(evil)
        assert out.startswith("`sha256:") and "evil" not in out and "<" not in out
