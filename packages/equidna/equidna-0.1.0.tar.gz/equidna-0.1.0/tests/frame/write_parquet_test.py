from __future__ import annotations

import pytest

from equidna.dataframe import DataFrame

data = {"a": [1, 2, 3]}


def test_write_parquet(tmpdir: pytest.TempdirFactory) -> None:
    path = tmpdir / "foo.parquet"  # type: ignore[operator]
    DataFrame(data).write_parquet(str(path))
    assert path.exists()
