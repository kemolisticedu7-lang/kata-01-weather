import csv
from pathlib import Path


DATA_FILE = Path("foundation-3/data/raw/flights_sample.csv")


def acquire_data():
    """Load flight delay data from CSV"""

    if not DATA_FILE.exists():
        print("Data file not found:", DATA_FILE)
        return []

    rows = []

    with open(DATA_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            rows.append(row)

    return rows


if __name__ == "__main__":
    data = acquire_data()

    print("Rows loaded:", len(data))

    if data:
        print("Sample row:", data[0])