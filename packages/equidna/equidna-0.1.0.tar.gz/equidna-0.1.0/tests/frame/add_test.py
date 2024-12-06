import pandas as pd

from equidna.dataframe import col, DataFrame
from tests.frame.util import assert_frame_equal


def test_add():
    data = {"a": [1, 3, 2], "b": [4, 4, 6], "z": [7.0, 8, 9]}
    df = DataFrame(data)

    actual = df.with_columns(
        c=col("a") + col("b"),
        d=col("a") - col("a").mean(),
        e=col("a") - col("a").std(),
    ).collect()

    expected = pd.DataFrame(
        {
            "a": [1, 3, 2],
            "b": [4, 4, 6],
            "z": [7.0, 8.0, 9.0],
            "c": [5, 7, 8],
            "d": [-1.0, 1.0, 0.0],
            "e": [0.0, 2.0, 1.0],
        }
    )

    assert_frame_equal(actual, expected)
