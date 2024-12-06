import polars as pl

import pytest


@pytest.fixture(scope="session")
def data():
    return pl.DataFrame(
        data={
            "name": ["Alice Archer", "Ben Brown", "Chloe Cooper", "Daniel Donovan"],
            "weight": [57.9, 72.5, 53.6, 83.1],  # (kg)
            "height": [1.56, 1.77, 1.65, 1.75],  # (m)
        }
    )
