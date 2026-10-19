import pytest


@pytest.fixture(autouse=True)
def isolated_mlflow(tmp_path, monkeypatch):
    """Isolate MLflow from the real server and the project directory."""
    monkeypatch.setenv(
        "MLFLOW_TRACKING_URI", f"sqlite:///{(tmp_path / 'mlflow.db').as_posix()}"
    )
    monkeypatch.chdir(tmp_path)
