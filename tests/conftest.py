import pytest


@pytest.fixture(autouse=True)
def isolated_mlflow(tmp_path, monkeypatch):
    """Point MLflow to a throwaway SQLite DB so tests never touch the real server."""
    monkeypatch.setenv(
        "MLFLOW_TRACKING_URI", f"sqlite:///{(tmp_path / 'mlflow.db').as_posix()}"
    )
