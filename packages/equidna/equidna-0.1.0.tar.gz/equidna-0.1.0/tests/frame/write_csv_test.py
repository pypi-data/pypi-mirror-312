from __future__ import annotations

from typing import TYPE_CHECKING

from equidna.dataframe import DataFrame

if TYPE_CHECKING:
    import pytest


def test_write_csv(tmpdir: pytest.TempdirFactory) -> None:
    data = {"a": [1, 2, 3]}
    path = tmpdir / "foo.csv"  # type: ignore[operator]
    result = DataFrame(data).write_csv(str(path))
    assert path.exists()
    assert result is None
