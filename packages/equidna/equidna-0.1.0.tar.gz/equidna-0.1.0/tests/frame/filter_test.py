from __future__ import annotations

import pandas as pd

from equidna.dataframe import DataFrame, col
from tests.frame.util import assert_frame_equal

import pytest


def test_filter() -> None:
    data = {"a": [1, 3, 2], "b": [4, 4, 6], "z": [7.0, 8, 9]}
    df = DataFrame(data)
    result = df.filter(col("a") > 1).collect()
    expected = pd.DataFrame({"a": [3, 2], "b": [4, 6], "z": [8.0, 9.0]})

    assert_frame_equal(result, expected)


@pytest.mark.xfail(raises=AssertionError)
def test_filter_with_boolean_list() -> None:
    data = {"a": [1, 3, 2], "b": [4, 4, 6], "z": [7.0, 8, 9]}
    df = DataFrame(data).collect()

    result = df.filter([False, True, True])
    expected = pd.DataFrame({"a": [3, 2], "b": [4, 6], "z": [8.0, 9.0]})
    assert_frame_equal(result, expected)
