from __future__ import annotations

import pytest

import pandas as pd

from equidna.dataframe import DataFrame
from tests.frame.util import assert_frame_equal


def test_sort() -> None:
    data = {"a": [1, 3, 2], "b": [4, 4, 6], "z": [7.0, 8, 9]}
    df = DataFrame(data)
    result = df.sort("a", "b").collect()
    expected = pd.DataFrame(
        {
            "a": [1, 2, 3],
            "b": [4, 6, 4],
            "z": [7.0, 9.0, 8.0],
        }
    )
    assert_frame_equal(result, expected)
    result = df.sort("a", "b", descending=[True, False]).collect()
    expected = pd.DataFrame(
        {
            "a": [3, 2, 1],
            "b": [4, 6, 4],
            "z": [8.0, 9.0, 7.0],
        }
    )
    assert_frame_equal(result, expected)


@pytest.mark.parametrize(
    ("nulls_last", "expected"),
    [
        (True, {"a": [0, 2, 0, -1], "b": [3, 2, 1, float("nan")]}),
        (False, {"a": [-1, 0, 2, 0], "b": [float("nan"), 3, 2, 1]}),
    ],
)
@pytest.mark.xfail(reason="not implemented")
def test_sort_nulls(nulls_last: bool, expected: dict[str, float]) -> None:
    data = {"a": [0, 0, 2, -1], "b": [1, 3, 2, None]}
    df = DataFrame(data)
    result = df.sort("b", descending=True, nulls_last=nulls_last)
    assert_frame_equal(result, pd.DataFrame(expected))
