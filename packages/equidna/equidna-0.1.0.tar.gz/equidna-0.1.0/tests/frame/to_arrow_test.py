from __future__ import annotations

import pyarrow as pa

from equidna.dataframe import DataFrame


def test_to_arrow() -> None:
    data = {"a": [1, 3, 2], "b": [4, 4, 6], "z": [7.1, 8, 9]}
    result = DataFrame(data).to_arrow()

    expected = pa.table(data)
    assert result == expected
