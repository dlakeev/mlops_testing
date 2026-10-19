from pathlib import Path

import pandas as pd
import yaml
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split


def split_data(
    df: pd.DataFrame,
    test_size: float,
    seed: int,
    stratify: bool = True,
    shuffle: bool = True,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split a dataframe into train and test parts."""
    train_df, test_df = train_test_split(
        df,
        test_size=test_size,
        shuffle=shuffle,
        stratify=df["target"] if stratify else None,
        random_state=seed,
    )
    return train_df, test_df


def prepare_data(params: dict, data_dir: Path) -> None:
    """Load raw data, split it and save CSV files to data_dir."""
    data_dir.mkdir(parents=True, exist_ok=True)

    df = load_breast_cancer(as_frame=True).frame
    df.to_csv(data_dir / "raw.csv", index=False, lineterminator="\n")

    train_df, test_df = split_data(df, seed=params["seed"], **params["split"])
    train_df.to_csv(data_dir / "train.csv", index=False, lineterminator="\n")
    test_df.to_csv(data_dir / "test.csv", index=False, lineterminator="\n")


if __name__ == "__main__":
    with open("params.yaml", encoding="utf-8") as f:
        params = yaml.safe_load(f)
    prepare_data(params, Path("data"))
