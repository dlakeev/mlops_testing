import pandas as pd
import pytest

from mlops_testing.prepare import split_data


@pytest.fixture
def df() -> pd.DataFrame:
    """Small synthetic dataset: 100 rows, imbalanced target (70/30)."""
    return pd.DataFrame(
        {
            "feature": range(100),
            "target": [0] * 70 + [1] * 30,
        }
    )


def test_split_has_no_overlap(df):
    train_df, test_df = split_data(df, test_size=0.2, seed=42)

    assert set(train_df.index).isdisjoint(test_df.index)
    assert len(train_df) + len(test_df) == len(df)


def test_split_sizes(df):
    train_df, test_df = split_data(df, test_size=0.2, seed=42)

    assert len(train_df) == 80
    assert len(test_df) == 20


def test_split_is_stratified(df):
    train_df, test_df = split_data(df, test_size=0.2, seed=42, stratify=True)

    train_ratio = train_df["target"].value_counts(normalize=True)

    assert train_ratio[1] == pytest.approx(0.3)


def test_split_is_reproducible(df):
    train_df1, test_df1 = split_data(df, test_size=0.2, seed=42)
    train_df2, test_df2 = split_data(df, test_size=0.2, seed=42)

    assert train_df1.equals(train_df2)
    assert test_df1.equals(test_df2)
