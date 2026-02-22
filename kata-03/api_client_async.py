import os
import time
import json
import requests

BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
OUTPUT_DIR = "kata-03/output"


def request_with_retry(params, retries=5, timeout=30):
    for attempt in range(retries):
        try:
            response = requests.get(BASE_URL, params=params, timeout=timeout)

            if response.status_code == 200:
                return response.json()

            if response.status_code in (429, 500, 502, 503, 504):
                wait_time = 2 ** attempt
                print(f"HTTP {response.status_code}. Retrying in {wait_time}s...")
                time.sleep(wait_time)
                continue

            print(f"HTTP Error {response.status_code}")
            return None

        except requests.RequestException as e:
            wait_time = 2 ** attempt
            print(f"Request failed: {e}. Retrying in {wait_time}s...")
            time.sleep(wait_time)

    return None


def fetch_all_observations(series_id, api_key):
    all_data = []
    offset = 0
    limit = 1000

    while True:
        params = {
            "series_id": series_id,
            "api_key": api_key,
            "file_type": "json",
            "limit": limit,
            "offset": offset,
        }

        data = request_with_retry(params)
        if not data:
            break

        observations = data.get("observations", [])
        all_data.extend(observations)

        print(f"Fetched {len(observations)} records (offset={offset})")

        if len(observations) < limit:
            break

        offset += limit
        time.sleep(0.25)

    return all_data


def save_json(series_id, data):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    file_path = os.path.join(OUTPUT_DIR, f"{series_id}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Saved to {file_path}")


def main():
    api_key = os.getenv("FRED_API_KEY")
    if not api_key:
        print("FRED_API_KEY not set.")
        return

    series_id = "UNRATE"
    observations = fetch_all_observations(series_id, api_key)

    if observations:
        save_json(series_id, observations)
    else:
        print("No data fetched.")


if __name__ == "__main__":
    main()