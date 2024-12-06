from __future__ import annotations

import pandas as pd

from equidna.dataframe import DataFrame


def test_to_dict() -> None:
    data = {"a": [1, 3, 2], "b": [4, 4, 6], "c": [7.0, 8, 9]}
    df = DataFrame(data)
    result = df.to_dict(as_series=False)
    assert result == data


def test_to_dict_as_series() -> None:
    data = {"a": [1, 3, 2], "b": [4, 4, 6], "c": [7.0, 8, 9]}
    df = DataFrame(data)
    result = df.to_dict(as_series=True)
    assert isinstance(result["a"], pd.Series)
    assert isinstance(result["b"], pd.Series)
    assert isinstance(result["c"], pd.Series)

    assert all(result[k].to_list() == v for k, v in data.items())
