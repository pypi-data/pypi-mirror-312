from __future__ import annotations

import numpy as np
import pandas as pd

import pytest

from equidna.dataframe import DataFrame, col
from tests.frame.util import assert_frame_equal

data = {
    "a": ["foo", "bars"],
    "ab": ["foo", "bars"],
}


@pytest.mark.xfail
def test_with_columns() -> None:
    result = (
        DataFrame(data)
        .with_columns(d=np.array([4, 5]))
        .with_columns(e=col("d") + 1)
        .select("d", "e")
    )
    expected = pd.DataFrame({"d": [4, 5], "e": [5, 6]})
    assert_frame_equal(result, expected)
