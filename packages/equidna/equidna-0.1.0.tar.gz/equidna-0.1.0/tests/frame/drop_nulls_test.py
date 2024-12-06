from __future__ import annotations

import pytest
import pandas as pd

from equidna.dataframe import DataFrame
from tests.frame.util import assert_frame_equal

data = {
    "a": [1.0, 2.0, None, 4.0],
    "b": [None, 3.0, None, 5.0],
}


def test_drop_nulls():
    result = DataFrame(data).drop_nulls().collect()
    expected = pd.DataFrame(
        {
            "a": [2.0, 4.0],
            "b": [3.0, 5.0],
        }
    )

    assert_frame_equal(result, expected)


@pytest.mark.parametrize(
    ("subset", "expected"),
    [
        ("a", {"a": [1, 2.0, 4.0], "b": [float("nan"), 3.0, 5.0]}),
        (["a"], {"a": [1, 2.0, 4.0], "b": [float("nan"), 3.0, 5.0]}),
        (["a", "b"], {"a": [2.0, 4.0], "b": [3.0, 5.0]}),
    ],
)
def test_drop_nulls_subset(subset: str | list[str], expected: dict[str, float]):
    result = DataFrame(data).drop_nulls(subset=subset).collect()
    assert_frame_equal(result, pd.DataFrame(expected))
