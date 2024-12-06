from __future__ import annotations

import pandas as pd
import pytest

from equidna.dataframe import DataFrame
from tests.frame.util import assert_frame_equal

import pyarrow as pa

data = {
    "a": ["x", "y", "z"],
    "b": [1, 3, 5],
    "c": [2, 4, 6],
}

expected_b_only = {
    "a": ["x", "y", "z"],
    "variable": ["b", "b", "b"],
    "value": [1, 3, 5],
}

expected_b_c = {
    "a": ["x", "y", "z", "x", "y", "z"],
    "variable": ["b", "b", "b", "c", "c", "c"],
    "value": [1, 3, 5, 2, 4, 6],
}


@pytest.mark.parametrize(
    ("on", "expected"),
    [("b", expected_b_only), (["b", "c"], expected_b_c), (None, expected_b_c)],
)
def test_unpivot_on(
    on: str | list[str] | None,
    expected: dict[str, list[float]],
) -> None:
    df = DataFrame(data)
    result = df.unpivot(on=on, index=["a"]).sort("variable", "a").collect()
    assert_frame_equal(result, pd.DataFrame(expected))


@pytest.mark.parametrize(
    ("variable_name", "value_name"),
    [
        ("custom_variable_name", "custom_value_name"),
    ],
)
def test_unpivot_var_value_names(
    variable_name: str | None,
    value_name: str | None,
) -> None:
    # FIXME problem with empty string as column names
    df = DataFrame(data)
    result = df.unpivot(
        on=["b", "c"], index=["a"], variable_name=variable_name, value_name=value_name
    ).collect()

    assert list(result.columns)[-2:] == [variable_name, value_name]


def test_unpivot_default_var_value_names() -> None:
    df = DataFrame(data)
    result = df.unpivot(on=["b", "c"], index=["a"])

    assert list(result.columns)[-2:] == ["variable", "value"]


@pytest.mark.parametrize(
    ("data", "expected_dtypes"),
    [
        (
            {"idx": [0, 1], "a": [1, 2], "b": [1.5, 2.5]},
            [pa.int64(), pa.string(), pa.float64()],
        ),
    ],
)
def test_unpivot_mixed_types(data, expected_dtypes) -> None:
    df = DataFrame(data)
    result = df.unpivot(on=["a", "b"], index="idx")

    # FIXME no access private field expr
    assert result.expr.schema().to_pyarrow().types == expected_dtypes
