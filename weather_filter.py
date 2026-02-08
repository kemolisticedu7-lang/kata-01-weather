import argparse
import csv
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Filter weather station data by temperature.")
    parser.add_argument("input_path", help="Path to the input CSV file")
    parser.add_argument("output_path", help="Path to the output CSV file")
    parser.add_argument("--min-temp", type=float, required=True, help="Minimum temperature threshold")
    args = parser.parse_args()

    input_path = Path(args.input_path)
    output_path = Path(args.output_path)

    if not input_path.exists():
        print(f"Error: input file not found: {input_path}")
        return 1

    # READ CSV
    with input_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        records = list(reader)

    # FILTER
    filtered = []
    for row in records:
        try:
            if float(row["temperature"]) >= args.min_temp:
                filtered.append(row)
        except:
            continue

    # WRITE OUTPUT
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(filtered)

    print(f"Read {len(records)} records")
    print(f"Wrote {len(filtered)} records to {output_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())