from equidna.dataframe import DataFrame, col
from tests.frame.util import assert_frame_equal

import polars as pl


def test_select(data):
    df = DataFrame(data)

    actual = df.select("name", weight_in_kg="weight").collect()
    expected = data.select("name", weight_in_kg="weight").to_pandas()

    assert_frame_equal(actual, expected)


def test_select_transform(data):
    df = DataFrame(data)

    actual = df.select(bmi=col("weight") / (col("height") * col("height"))).collect()
    expected = data.select(
        bmi=pl.col("weight") / (pl.col("height") * pl.col("height"))
    ).to_pandas()

    assert_frame_equal(actual, expected)


def test_head(data):
    df = DataFrame(data)

    actual = df.head().collect()
    expected = data.head().to_pandas()

    assert_frame_equal(actual, expected, check_dtype=False)
