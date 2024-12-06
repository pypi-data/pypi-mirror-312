from __future__ import annotations

import pandas as pd

from equidna.dataframe import DataFrame
from tests.frame.util import assert_frame_equal


def test_rename() -> None:
    data = {"a": [1, 3, 2], "b": [4, 4, 6], "z": [7.0, 8, 9]}
    df = DataFrame(data)
    result = df.rename({"a": "x", "b": "y"}).collect()
    expected = pd.DataFrame({"x": [1, 3, 2], "y": [4, 4, 6], "z": [7.0, 8, 9]})
    assert_frame_equal(result, expected)
