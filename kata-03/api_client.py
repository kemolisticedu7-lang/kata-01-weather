import os
import time
import json
import requests

BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
OUTPUT_DIR = "kata-03/output"


def request_with_retry(params, retries=7, timeout=20):
    for attempt in range(retries):
        try:
            r = requests.get(BASE_URL, params=params, timeout=timeout)

            if r.status_code == 200:
                return r.json()

            if r.status_code in (429, 500, 502, 503, 504):
                wait = 2 ** attempt
                print(f"HTTP {r.status_code}. Retrying in {wait}s...")
                time.sleep(wait)
                continue

            print(f"HTTP Error {r.status_code}: {r.text[:120]}")
            return None

        except requests.RequestException as e:
            wait = 2 ** attempt
            print(f"Request failed: {e}. Retrying in {wait}s...")
            time.sleep(wait)

    return None


def fetch_all_observations(series_id, api_key, limit=1000):
    all_obs = []
    offset = 0

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

        obs = data.get("observations", [])
        all_obs.extend(obs)

        print(f"Fetched {len(obs)} records (offset={offset})")

        if len(obs) < limit:
            break

        offset += limit
        time.sleep(0.25)  # rate limit safety

    return all_obs


def save_json(series_id, observations):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, f"{series_id}.json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(observations, f, indent=2)

    print(f"Saved: {out_path}")


def main():
    api_key = os.getenv("FRED_API_KEY")
    if not api_key:
        print("Missing FRED_API_KEY. Set it in the terminal first.")
        return

    series_id = "UNRATE"
    observations = fetch_all_observations(series_id, api_key)

    if observations:
        save_json(series_id, observations)
    else:
        print("No observations fetched.")


if __name__ == "__main__":
    main()