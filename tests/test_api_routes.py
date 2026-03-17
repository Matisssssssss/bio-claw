from app.api.main import health, strategies


def test_api_function_routes_basic() -> None:
    assert health()['status'] == 'ok'
    assert isinstance(strategies(), list)
