import csv
from datetime import datetime

INPUT_FILE = "sample_weather.csv"
OUTPUT_FILE = "output/delay_risk_scores.csv"


def create_output_folder():
    import os
    os.makedirs("output", exist_ok=True)


def load_data():
    with open(INPUT_FILE, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)


def transform_data(data):
    results = []

    for row in data:
        # Example feature: temperature as proxy
        temp = float(row.get("temperature", 0))

        # Fake "delay risk" logic (acceptable MVP)
        if temp > 80:
            risk = 0.7
        elif temp > 60:
            risk = 0.5
        else:
            risk = 0.2

        results.append({
            "date": row.get("date"),
            "temperature": temp,
            "delay_risk": risk
        })

    return results


def save_results(data):
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "temperature", "delay_risk"])
        writer.writeheader()
        writer.writerows(data)


def run_pipeline():
    print("Running pipeline...")

    create_output_folder()
    raw_data = load_data()
    transformed = transform_data(raw_data)
    save_results(transformed)

    print("Pipeline complete. Output saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    run_pipeline()