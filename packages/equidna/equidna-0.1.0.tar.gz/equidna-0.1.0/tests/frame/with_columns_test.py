from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from equidna.dataframe import DataFrame, col
from tests.frame.util import assert_frame_equal


@pytest.mark.xfail
def test_with_columns_int_col_name_pandas() -> None:
    np_matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    df = pd.DataFrame(np_matrix, dtype="int64")
    ed_df = DataFrame(df)
    result = ed_df.with_columns(ed_df.get_column(1).alias(4))  # type: ignore[arg-type]
    expected = pd.DataFrame(
        {0: [1, 4, 7], 1: [2, 5, 8], 2: [3, 6, 9], 4: [2, 5, 8]}, dtype="int64"
    )
    pd.testing.assert_frame_equal(result, expected)


def test_with_columns_order() -> None:
    # FIXME with_columns is a mixture of mutate with select or simple keep the name a
    data = {"a": [1, 3, 2], "b": [4, 4, 6], "z": [7.0, 8, 9]}
    df = DataFrame(data)
    result = df.with_columns(a=col("a") + 1, d=col("a") - 1).collect()
    assert list(result.columns) == ["a", "b", "z", "d"]
    expected = pd.DataFrame(
        {"a": [2, 4, 3], "b": [4, 4, 6], "z": [7.0, 8, 9], "d": [0, 2, 1]}
    )
    assert_frame_equal(result, expected)


@pytest.mark.xfail(reason="empty selection not implemented")
def test_with_columns_empty() -> None:
    data = {"a": [1, 3, 2], "b": [4, 4, 6], "z": [7.0, 8, 9]}
    df = DataFrame(data)
    result = df.select().with_columns()
    assert_frame_equal(result, pd.DataFrame())


# FIXME implement single row selection
