import sys
from pathlib import Path

sys.path.append(str(Path("foundation-3/src").resolve()))

from run_pipeline import run_pipeline


def test_pipeline():
    run_pipeline()


if __name__ == "__main__":
    test_pipeline()
    print("test_pipeline passed")