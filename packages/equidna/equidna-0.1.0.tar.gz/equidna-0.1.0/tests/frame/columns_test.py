from equidna.dataframe import DataFrame


def test_columns() -> None:
    data = {"a": [1, 3, 2], "b": [4, 4, 6], "z": [7.0, 8, 9]}
    df = DataFrame(data)
    result = df.columns
    expected = ["a", "b", "z"]
    assert result == expected
