from __future__ import annotations

import pandas as pd

from equidna.dataframe import DataFrame, col
from equidna.selectors import all
from tests.frame.util import assert_frame_equal


def test_all():
    data = {"a": [1, 3, 2], "b": [4, 4, 6], "z": [7.0, 8, 9]}
    df = DataFrame(data)

    result = df.with_columns(all() * 2).collect()
    expected = pd.DataFrame({"a": [2, 6, 4], "b": [8, 8, 12], "z": [14.0, 16.0, 18.0]})

    assert_frame_equal(result, expected)


def test_all_double():
    # FIXME the methods should return new expressions each time
    # FIXME order of columns in with_columns

    data = {"a": [1, 3, 2], "b": [4, 4, 6], "z": [7.0, 8, 9]}
    df = DataFrame(data)

    # FIXME change name to alias
    result = df.with_columns(col("a").name("o"), all() * 2).collect()
    expected = pd.DataFrame(
        {
            "a": [2, 6, 4],
            "b": [8, 8, 12],
            "z": [14.0, 16.0, 18.0],
            "o": [1, 3, 2],
        }
    )

    assert_frame_equal(result, expected)
