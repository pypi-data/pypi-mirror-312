from __future__ import annotations

import pandas as pd
import pytest

from equidna.dataframe import DataFrame
from tests.frame.util import assert_frame_equal

data = {"a": [1, 3, 2], "b": [4, 4, 6], "z": [7.0, 8, 9]}


@pytest.mark.parametrize("subset", ["b", ["b"]])
@pytest.mark.parametrize(
    ("keep", "expected"),
    [
        ("first", {"a": [1, 2], "b": [4, 6], "z": [7.0, 9.0]}),
        ("last", {"a": [2, 3], "b": [6, 4], "z": [9.0, 8.0]}),
    ],
)
def test_unique(
    subset: str | list[str] | None,
    keep: str,
    expected: dict[str, list[float]],
) -> None:
    df = DataFrame(data)

    result = df.unique(subset, keep=keep).sort("a").collect()  # type: ignore[arg-type]
    assert_frame_equal(result, pd.DataFrame(expected))
