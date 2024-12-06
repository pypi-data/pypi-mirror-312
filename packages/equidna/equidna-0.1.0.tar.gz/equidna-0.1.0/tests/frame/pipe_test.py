from __future__ import annotations

import pandas as pd

from equidna.dataframe import DataFrame
from tests.frame.util import assert_frame_equal

data = {
    "a": ["foo", "bars"],
    "ab": ["foo", "bars"],
}


def test_pipe() -> None:
    df = DataFrame(data)
    columns = list(df.collect().columns)
    result = df.pipe(
        lambda _df: _df.select([x for x in columns if len(x) == 2])
    ).collect()
    expected = pd.DataFrame({"ab": ["foo", "bars"]})
    assert_frame_equal(result, expected)
