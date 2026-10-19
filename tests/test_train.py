import json

import pytest

from mlops_testing.prepare import prepare_data
from mlops_testing.train import build_pipeline, train


@pytest.fixture
def params() -> dict:
    """Default parameters for the pipeline."""
    return {
        "seed": 42,
        "split": {"test_size": 0.2, "stratify": True},
        "pipeline": {"model__max_iter": 200},
    }


def test_build_pipeline_applies_params():
    params = {"model__max_iter": 200}
    seed = 7
    pipe = build_pipeline(params, seed)

    assert pipe.named_steps["model"].max_iter == 200
    assert pipe.named_steps["model"].random_state == seed


def test_build_pipeline_raise_invalid_params():
    params = {"model__max_iters": 200}

    with pytest.raises(ValueError, match="Invalid parameter 'max_iters'"):
        build_pipeline(params, 42)


def test_pipeline_creates_artifacts(tmp_path, params):
    data_dir = tmp_path / "data"
    models_dir = tmp_path / "models"
    metrics_dir = tmp_path / "metrics"

    prepare_data(params, data_dir)
    train(params, data_dir, models_dir, metrics_dir)

    assert (models_dir / "model.joblib").exists()
    assert (metrics_dir / "metrics.json").exists()

    with open(metrics_dir / "metrics.json") as f:
        metrics = json.load(f)
        assert all(0 <= value <= 1 for value in metrics.values())
