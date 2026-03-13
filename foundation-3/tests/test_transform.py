import sys
from pathlib import Path
import pytest

sys.path.append(str(Path("foundation-3/src").resolve()))

from transform_data import transform_data


@pytest.mark.parametrize("expected_rows", [9])
def test_transform(expected_rows):
    rows = transform_data()
    assert len(rows) == 99