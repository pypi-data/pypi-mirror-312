from __future__ import annotations

import pytest

from equidna.dataframe import DataFrame


@pytest.mark.xfail
def test_sample_fraction() -> None:
    df = DataFrame({"a": [1, 2, 3, 4], "b": ["x", "y", "x", "y"]})

    result_expr = df.sample(fraction=0.5).collect().shape
    expected_expr = (2, 2)
    assert result_expr == expected_expr
