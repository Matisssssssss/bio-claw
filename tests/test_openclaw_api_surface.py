from app.openclaw.api import list_tools, openclaw_health


def test_openclaw_api_functions() -> None:
    health = openclaw_health()
    assert health.ready is True
    tools = list_tools()
    assert len(tools) >= 3
