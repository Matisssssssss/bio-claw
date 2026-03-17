from app.cli import app


def test_cli_app_exists() -> None:
    assert app is not None
