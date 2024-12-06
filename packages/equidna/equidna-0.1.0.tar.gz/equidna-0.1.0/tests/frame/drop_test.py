from __future__ import annotations

import pytest

from equidna.dataframe import DataFrame


# FIXME add checks for exceptions
# FIXME verify that list can be passed the same as narwhals


@pytest.mark.parametrize(
    ("to_drop", "expected"),
    [
        ("abc", ["b", "z"]),
        (["abc"], ["b", "z"]),
        (["abc", "b"], ["z"]),
    ],
)
def test_drop(to_drop: list[str], expected: list[str]) -> None:
    data = {"abc": [1, 3, 2], "b": [4, 4, 6], "z": [7.0, 8, 9]}
    df = DataFrame(data)

    if not isinstance(to_drop, str):
        assert list(df.drop(*to_drop).collect().columns) == expected
    else:
        assert list(df.drop(to_drop).collect().columns) == expected
