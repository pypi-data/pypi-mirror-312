from __future__ import annotations

import pandas as pd

from equidna.dataframe import DataFrame
from tests.frame.util import assert_frame_equal


def test_head() -> None:
    data = {"a": [1, 3, 2], "b": [4, 4, 6], "z": [7.0, 8, 9]}
    expected = pd.DataFrame({"a": [1, 3], "b": [4, 4], "z": [7.0, 8.0]})

    df = DataFrame(data)

    result = df.head(2).collect()
    assert_frame_equal(result, expected)
