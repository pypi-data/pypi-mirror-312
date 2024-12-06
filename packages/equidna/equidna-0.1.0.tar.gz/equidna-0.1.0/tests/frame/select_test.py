from __future__ import annotations

import pandas as pd

from equidna.dataframe import DataFrame
from tests.frame.util import assert_frame_equal


# FIXME add non string select
# FIXME add empty select


def test_select() -> None:
    data = {"a": [1, 3, 2], "b": [4, 4, 6], "z": [7.0, 8, 9]}
    df = DataFrame(data)
    result = df.select("a").collect()
    expected = pd.DataFrame({"a": [1, 3, 2]})
    assert_frame_equal(result, expected)
