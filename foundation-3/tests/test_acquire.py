import sys
from pathlib import Path

sys.path.append(str(Path("foundation-3/src").resolve()))

from acquire_data import acquire_data


def test_acquire():
    rows = acquire_data()
    assert len(rows) == 10


if __name__ == "__main__":
    test_acquire()
    print("test_acquire passed")