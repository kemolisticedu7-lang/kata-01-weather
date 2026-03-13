import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.append(str(SCRIPT_DIR))

from acquire_data import acquire_data
from transform_data import transform_data


def run_pipeline():
    print("Starting pipeline...")

    raw = acquire_data()
    print("Acquired rows:", len(raw))

    cleaned = transform_data()
    print("Transformed rows:", len(cleaned))

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()