import csv
from pathlib import Path


INPUT_FILE = Path("foundation-3/data/raw/flights_sample.csv")
OUTPUT_FILE = Path("foundation-3/data/transformed/flights_cleaned.csv")


def transform_data():
    """Clean and transform flight delay data"""

    rows = []

    with open(INPUT_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:

            delay = row["DepDelay"]

            if delay == "" or delay is None:
                continue

            row["DepDelay"] = float(delay)

            rows.append(row)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["FlightDate", "Carrier", "Origin", "Dest", "DepDelay"]
        )

        writer.writeheader()
        writer.writerows(rows)

    return rows


if __name__ == "__main__":
    cleaned = transform_data()

    print("Rows after cleaning:", len(cleaned))