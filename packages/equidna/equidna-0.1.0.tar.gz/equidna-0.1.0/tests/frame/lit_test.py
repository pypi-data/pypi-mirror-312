from __future__ import annotations

from typing import Any

import ibis.expr.datatypes as dt
import pandas as pd
import pytest

from equidna.dataframe import DataFrame, lit
from tests.frame.util import assert_frame_equal


@pytest.mark.parametrize(
    ("dtype", "expected_lit"),
    [(None, [2, 2, 2]), (dt.string, ["2", "2", "2"]), (dt.float32, [2.0, 2.0, 2.0])],
)
def test_lit(dtype, expected_lit: list[Any]) -> None:
    data = {"a": [1, 3, 2], "b": [4, 4, 6], "z": [7.0, 8, 9]}
    df = DataFrame(data)
    result = df.with_columns(lit(2, dtype).name("lit")).collect()
    expected = pd.DataFrame(
        {
            "a": [1, 3, 2],
            "b": [4, 4, 6],
            "z": [7.0, 8.0, 9.0],
            "lit": expected_lit,
        }
    )
    assert_frame_equal(result, expected, check_dtype=False)


# FIXME dtypes issues
# FIXME create own Ibis types


def test_lit_out_name() -> None:
    data = {"a": [1, 3, 2]}
    df = DataFrame(data)
    result = df.with_columns(lit(2).name("literal")).collect()
    expected = pd.DataFrame(
        {
            "a": [1, 3, 2],
            "literal": [2, 2, 2],
        }
    )
    assert_frame_equal(result, expected, check_dtype=False)
