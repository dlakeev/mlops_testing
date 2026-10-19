from pathlib import Path

import yaml
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split


def prepare_data():
    # Load parameters from yaml file
    with open("./params.yaml", encoding="utf-8") as f:
        params = yaml.safe_load(f)

    # Load data
    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)
    df = load_breast_cancer(as_frame=True).frame
    df.to_csv(data_dir / "raw.csv", index=False)

    # Split data into training and testing sets
    split = dict(params["split"])
    use_stratify = split.pop("stratify", False)

    train_df, test_df = train_test_split(
        df,
        **split,
        stratify=df["target"] if use_stratify else None,
        random_state=params["seed"],
    )

    train_df.to_csv(data_dir / "train.csv", index=False)
    test_df.to_csv(data_dir / "test.csv", index=False)


if __name__ == "__main__":
    prepare_data()
