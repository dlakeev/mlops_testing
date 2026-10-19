import json
from pathlib import Path

import joblib
import mlflow
import pandas as pd
import yaml
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def build_pipeline(pipeline_params: dict, seed: int) -> Pipeline:
    """Create an unfitted scaler + logistic regression pipeline."""
    pipe = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("model", LogisticRegression()),
        ]
    )
    pipe.set_params(model__random_state=seed, **pipeline_params)
    return pipe


def evaluate(model: Pipeline, X: pd.DataFrame, y: pd.Series) -> dict[str, float]:
    """Compute classification metrics for binary classification."""
    y_pred = model.predict(X)
    y_pred_proba = model.predict_proba(X)[:, 1]
    return {
        "accuracy": accuracy_score(y, y_pred),
        "f1_score": f1_score(y, y_pred),
        "roc_auc": roc_auc_score(y, y_pred_proba),
    }


def train(params: dict, data_dir: Path, models_dir: Path, metrics_dir: Path) -> None:
    """Train on data_dir/train.csv, save the model and test metrics."""
    mlflow.set_experiment("breast-cancer")

    train_df = pd.read_csv(data_dir / "train.csv")
    test_df = pd.read_csv(data_dir / "test.csv")

    X_train, y_train = train_df.drop(columns="target"), train_df["target"]
    X_test, y_test = test_df.drop(columns="target"), test_df["target"]

    with mlflow.start_run():
        mlflow.log_params(_flatten_dict(params))

        pipe = build_pipeline(params["pipeline"], params["seed"])
        pipe.fit(X_train, y_train)

        models_dir.mkdir(parents=True, exist_ok=True)
        joblib.dump(pipe, models_dir / "model.joblib")

        eval_metrics = evaluate(pipe, X_test, y_test)

        mlflow.log_metrics(eval_metrics)

        metrics_dir.mkdir(parents=True, exist_ok=True)
        with open(
            metrics_dir / "metrics.json", "w", encoding="utf-8", newline="\n"
        ) as f:
            json.dump(eval_metrics, f, indent=2)
            f.write("\n")


def _flatten_dict(d: dict, parent_key: str = "", sep: str = ".") -> dict:
    """Flatten dict into a single level with keys joined by sep.
    Example: {"split": {"test_size": 0.2}} -> {"split.test_size": 0.2}
    """
    items = {}
    for key, value in d.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            items.update(_flatten_dict(value, new_key, sep))
        else:
            items[new_key] = value
    return items


if __name__ == "__main__":
    with open("params.yaml", encoding="utf-8") as f:
        params = yaml.safe_load(f)
    train(params, Path("data"), Path("models"), Path("metrics"))
