import pytest
from pathlib import Path


@pytest.fixture
def sample_csv(tmp_path):
    file = tmp_path / "sample.csv"

    file.write_text(
        "FlightDate,Carrier,Origin,Dest,DepDelay\n"
        "2023-01-01,AA,DFW,LAX,5\n"
        "2023-01-01,DL,ATL,JFK,-2\n",
        encoding="utf-8",
    )

    return file