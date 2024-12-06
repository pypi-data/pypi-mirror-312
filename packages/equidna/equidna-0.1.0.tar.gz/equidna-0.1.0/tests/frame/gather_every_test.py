import pandas as pd
import pytest

from equidna.dataframe import DataFrame
from tests.frame.util import assert_frame_equal

data = {"a": list(range(10))}


@pytest.mark.xfail(raises=AssertionError)
@pytest.mark.parametrize("n", [1, 2, 3])
@pytest.mark.parametrize("offset", [1, 2, 3])
def test_gather_every(n: int, offset: int) -> None:
    df = DataFrame(data)
    result = df.gather_every(n=n, offset=offset).collect()
    expected = pd.DataFrame({"a": data["a"][offset::n]})
    assert_frame_equal(result, expected)
