from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

import joblib
import json
import yaml
import pandas as pd
from pathlib import Path


def train():
    # Load parameters from yaml file
    with open("./params.yaml", encoding="utf-8") as f:
        params = yaml.safe_load(f)

    # Load and split data
    train_df = pd.read_csv("data/train.csv")
    test_df = pd.read_csv("data/test.csv")

    X_train, y_train = train_df.drop(columns="target"), train_df["target"]
    X_test, y_test = test_df.drop(columns="target"), test_df["target"]

    # Init pipeline
    pipe = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("model", LogisticRegression()),
        ]
    )
    pipe.set_params(model__random_state=params["seed"], **params["pipeline"])
    pipe.fit(X_train, y_train)

    models_dir = Path("models")
    models_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, models_dir / "model.joblib")

    # Calculate metrics
    y_pred = pipe.predict(X_test)
    y_pred_proba = pipe.predict_proba(X_test)[:, 1]
    accuracy, f1, roc_auc = (
        accuracy_score(y_test, y_pred),
        f1_score(y_test, y_pred),
        roc_auc_score(y_test, y_pred_proba),
    )

    # Save metrics
    metrics = {"accuracy": accuracy, "f1_score": f1, "roc_auc": roc_auc}
    metrics_dir = Path("metrics")
    metrics_dir.mkdir(parents=True, exist_ok=True)
    with open(metrics_dir / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)


if __name__ == "__main__":
    train()
