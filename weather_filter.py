import argparse 
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

    print(f"Input file exists: {input_path}")
    print(f"Output will be written to: {output_path}")
    print(f"Filtering with min temperature: {args.min_temp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())