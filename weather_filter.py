import argparse
import csv
from pathlib import Path
from datetime import datetime


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Filter weather station data by temperature threshold."
    )
    parser.add_argument("input_path", help="Path to the input CSV file")
    parser.add_argument("output_path", help="Path to the output CSV file")
    parser.add_argument(
        "--min-temp",
        type=float,
        required=True,
        help="Minimum temperature threshold",
    )
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
        fieldnames = reader.fieldnames or []

    # FILTER
    filtered = []
    for row in records:
        try:
            if float(row.get("temperature", "")) >= args.min_temp:
                filtered.append(row)
        except (ValueError, TypeError):
            # Skip rows with missing/bad temperature
            continue

    # WRITE OUTPUT
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered)

    print(f"Read {len(records)} records")
    print(f"Wrote {len(filtered)} records to {output_path}")

    # LOG (append mode)
    log_path = Path("weather_filter.log")
    timestamp = datetime.now().isoformat(timespec="seconds")
    with log_path.open("a", encoding="utf-8") as log_file:
        log_file.write(f"{timestamp} | read={len(records)} | wrote={len(filtered)}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())