from __future__ import annotations

import re
from typing import Any

import pandas as pd
import pytest

from equidna.dataframe import DataFrame, col
from tests.frame.util import assert_frame_equal


def test_inner_join_two_keys() -> None:
    # FIXME order of columns should match
    data = {
        "antananarivo": [1, 3, 2],
        "bob": [4, 4, 6],
        "zorro": [7.0, 8, 9],
        "index": [0, 1, 2],
    }
    df = DataFrame(data)
    df_right = df
    result = df.join(
        df_right,  # type: ignore[arg-type]
        left_on=["antananarivo", "bob"],
        right_on=["antananarivo", "bob"],
        how="inner",
    )
    result_on = df.join(df_right, on=["antananarivo", "bob"], how="inner")  # type: ignore[arg-type]
    result = result.sort("index").drop("index_right").collect()
    result_on = result_on.sort("index").drop("index_right").collect()
    expected = pd.DataFrame(
        {
            "antananarivo": [1, 3, 2],
            "bob": [4, 4, 6],
            "zorro": [7.0, 8, 9],
            "index": [0, 1, 2],
            "zorro_right": [7.0, 8, 9],
        }
    )
    assert_frame_equal(result, expected)
    assert_frame_equal(result_on, expected)


def test_inner_join_single_key() -> None:
    data = {
        "antananarivo": [1, 3, 2],
        "bob": [4, 4, 6],
        "zorro": [7.0, 8, 9],
        "index": [0, 1, 2],
    }
    df = DataFrame(data)
    df_right = df
    result = df.join(
        df_right,  # type: ignore[arg-type]
        left_on="antananarivo",
        right_on="antananarivo",
        how="inner",
    ).sort("index")
    result_on = df.join(df_right, on="antananarivo", how="inner").sort("index")  # type: ignore[arg-type]
    result = result.drop("index_right").collect()
    result_on = result_on.drop("index_right").collect()
    expected = pd.DataFrame(
        {
            "antananarivo": [1, 3, 2],
            "bob": [4, 4, 6],
            "zorro": [7.0, 8, 9],
            "index": [0, 1, 2],
            "bob_right": [4, 4, 6],
            "zorro_right": [7.0, 8, 9],
        }
    )

    assert_frame_equal(result, expected)
    assert_frame_equal(result_on, expected)


def test_cross_join() -> None:
    data = {"antananarivo": [1, 3, 2]}
    df = DataFrame(data)
    result = (
        df.join(df, how="cross").sort("antananarivo", "antananarivo_right").collect()
    )
    expected = pd.DataFrame(
        {
            "antananarivo": [1, 1, 1, 2, 2, 2, 3, 3, 3],
            "antananarivo_right": [1, 2, 3, 1, 2, 3, 1, 2, 3],
        }
    )
    assert_frame_equal(result, expected)


@pytest.mark.parametrize("how", ["inner"])
@pytest.mark.parametrize("suffix", ["_right", "_custom_suffix"])
def test_suffix(how: str, suffix: str) -> None:
    # FIXME problem with how = left
    data = {
        "antananarivo": [1, 3, 2],
        "bob": [4, 4, 6],
        "zorro": [7.0, 8, 9],
    }
    df = DataFrame(data)
    df_right = df
    result = df.join(
        df_right,  # type: ignore[arg-type]
        left_on=["antananarivo", "bob"],
        right_on=["antananarivo", "bob"],
        how=how,  # type: ignore[arg-type]
        suffix=suffix,
    ).collect()
    result_cols = list(result.columns)
    assert result_cols == ["antananarivo", "bob", "zorro", f"zorro{suffix}"]


@pytest.mark.parametrize("suffix", ["_right", "_custom_suffix"])
def test_cross_join_suffix(suffix: str) -> None:
    data = {"antananarivo": [1, 3, 2]}
    df = DataFrame(data)
    result = (
        df.join(df, how="cross", suffix=suffix)
        .sort(  # type: ignore[arg-type]
            "antananarivo", f"antananarivo{suffix}"
        )
        .collect()
    )
    expected = pd.DataFrame(
        {
            "antananarivo": [1, 1, 1, 2, 2, 2, 3, 3, 3],
            f"antananarivo{suffix}": [1, 2, 3, 1, 2, 3, 1, 2, 3],
        }
    )
    assert_frame_equal(result, expected)


def test_cross_join_non_pandas() -> None:
    data = {"antananarivo": [1, 3, 2]}
    df = DataFrame(pd.DataFrame(data))
    result = df.join(df, how="cross").collect()
    expected = pd.DataFrame(
        {
            "antananarivo": [1, 1, 1, 3, 3, 3, 2, 2, 2],
            "antananarivo_right": [1, 3, 2, 1, 3, 2, 1, 3, 2],
        }
    )
    assert_frame_equal(result, expected)


#
#
@pytest.mark.parametrize(
    ("join_key", "filter_expr", "expected"),
    [
        (
            ["antananarivo", "bob"],
            (col("bob") < 5),
            {"antananarivo": [2], "bob": [6], "zorro": [9]},
        ),
        (["bob"], (col("bob") < 5), {"antananarivo": [2], "bob": [6], "zorro": [9]}),
        (
            ["bob"],
            (col("bob") > 5),
            {"antananarivo": [1, 3], "bob": [4, 4], "zorro": [7.0, 8.0]},
        ),
    ],
)
def test_anti_join(
    join_key: list[str],
    filter_expr,
    expected: dict[str, list[Any]],
) -> None:
    data = {"antananarivo": [1, 3, 2], "bob": [4, 4, 6], "zorro": [7.0, 8, 9]}
    df = DataFrame(data)
    other = df.filter(filter_expr)
    result = df.join(other, how="anti", left_on=join_key, right_on=join_key).collect()  # type: ignore[arg-type]
    assert_frame_equal(
        result, pd.DataFrame(expected), check_dtype=False
    )  # FIXME check dtypes


@pytest.mark.parametrize(
    ("join_key", "filter_expr", "expected"),
    [
        (
            "antananarivo",
            (col("bob") > 5),
            {"antananarivo": [2], "bob": [6], "zorro": [9]},
        ),
        (
            ["antananarivo"],
            (col("bob") > 5),
            {"antananarivo": [2], "bob": [6], "zorro": [9]},
        ),
        (
            ["bob"],
            (col("bob") < 5),
            {"antananarivo": [1, 3], "bob": [4, 4], "zorro": [7, 8]},
        ),
        (
            ["antananarivo", "bob"],
            (col("bob") < 5),
            {"antananarivo": [1, 3], "bob": [4, 4], "zorro": [7, 8]},
        ),
    ],
)
def test_semi_join(
    join_key: list[str],
    filter_expr,
    expected: dict[str, list[Any]],
) -> None:
    data = {"antananarivo": [1, 3, 2], "bob": [4, 4, 6], "zorro": [7.0, 8, 9]}
    df = DataFrame(data)
    other = df.filter(filter_expr)
    result = (
        df.join(other, how="semi", left_on=join_key, right_on=join_key)
        .sort(  # type: ignore[arg-type]
            "antananarivo"
        )
        .collect()
    )

    assert_frame_equal(result, pd.DataFrame(expected), check_dtype=False)


@pytest.mark.parametrize("how", ["full"])
def test_join_not_implemented(how: str) -> None:
    data = {"antananarivo": [1, 3, 2], "bob": [4, 4, 6], "zorro": [7.0, 8, 9]}
    df = DataFrame(data)

    with pytest.raises(
        Exception,
        match=re.escape(
            "Expected signature: JoinLink(how: Literal['inner', 'left', 'right', 'outer', 'asof', 'semi', 'anti', 'any_inner', 'any_left', 'cross', 'positional']"
        ),
    ):
        df.join(df, left_on="antananarivo", right_on="antananarivo", how=how).collect()  # type: ignore[arg-type]


def test_join_asof_numeric() -> None:
    # FIXME order of rows

    df = DataFrame({"antananarivo": [1, 5, 10], "val": ["a", "b", "c"]}).sort(
        "antananarivo"
    )
    df_right = DataFrame(
        {"antananarivo": [1, 2, 3, 6, 7], "val": [1, 2, 3, 6, 7]}
    ).sort("antananarivo")
    result_backward = df.join_asof(
        df_right,  # type: ignore[arg-type]
        left_on="antananarivo",
        right_on="antananarivo",
    ).collect()
    result_forward = df.join_asof(
        df_right,  # type: ignore[arg-type]
        left_on="antananarivo",
        right_on="antananarivo",
        strategy="forward",
    ).collect()
    result_backward_on = df.join_asof(df_right, on="antananarivo").collect()
    result_forward_on = df.join_asof(
        df_right, on="antananarivo", strategy="forward"
    ).collect()
    expected_backward = pd.DataFrame(
        {
            "antananarivo": [1, 5, 10],
            "val": ["a", "b", "c"],
            "antananarivo_right": [1, 3, 7],
            "val_right": [1, 3, 7],
        }
    )
    expected_forward = pd.DataFrame(
        {
            "antananarivo": [5, 1, 10],
            "val": ["b", "a", "c"],
            "antananarivo_right": [6, 1, float("nan")],
            "val_right": [6, 1, float("nan")],
        }
    )
    assert_frame_equal(result_backward, expected_backward)
    assert_frame_equal(result_forward, expected_forward)
    assert_frame_equal(result_backward_on, expected_backward)
    assert_frame_equal(result_forward_on, expected_forward)


def test_join_asof_by() -> None:
    df = DataFrame(
        {
            "antananarivo": [1, 5, 7, 10],
            "bob": ["D", "D", "C", "A"],
            "c": [9, 2, 1, 1],
        }
    ).sort("antananarivo")
    df_right = DataFrame(
        {"antananarivo": [1, 4, 5, 8], "bob": ["D", "D", "A", "F"], "d": [1, 3, 4, 1]}
    ).sort("antananarivo")
    result = df.join_asof(
        df_right, on="antananarivo", by_left="bob", by_right="bob"
    ).collect()
    result_by = df.join_asof(df_right, on="antananarivo", by="bob").collect()
    expected = pd.DataFrame(
        {
            "antananarivo": [7, 10, 1, 5],
            "bob": ["C", "A", "D", "D"],
            "c": [1, 1, 9, 2],
            "antananarivo_right": [float("nan"), 5.0, 1.0, 4.0],
            "bob_right": [None, "A", "D", "D"],
            "d": [float("nan"), 4, 1, 3],
        }
    )
    assert_frame_equal(result, expected, check_dtype=False)
    assert_frame_equal(result_by, expected, check_dtype=False)
