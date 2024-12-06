from __future__ import annotations

from typing import Any

import pytest

from equidna.dataframe import DataFrame, col


@pytest.mark.parametrize(("threshold", "expected"), [(0, False), (10, True)])
def test_is_empty(threshold: Any, expected: Any) -> None:
    data = {"a": [1, 3, 2], "b": [4, 4, 6], "z": [7.0, 8, 9]}
    df = DataFrame(data)
    result = df.filter(col("a") > threshold).is_empty()
    assert result == expected
