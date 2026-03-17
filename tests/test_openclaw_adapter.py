from app.openclaw.adapter import OpenClawAdapter


def test_openclaw_registry_has_default_tools() -> None:
    adapter = OpenClawAdapter()
    names = {t.name for t in adapter.registry.list_tools()}
    assert 'biotech.research_ticker' in names
    assert 'biotech.canonical_catalysts' in names


def test_openclaw_exec_unknown_tool() -> None:
    adapter = OpenClawAdapter()
    result = adapter.registry.execute('unknown.tool', {})
    assert result.ok is False
