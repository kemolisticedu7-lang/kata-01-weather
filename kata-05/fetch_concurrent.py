import json
import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Tuple

import requests


BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"
OUTPUT_DIR = BASE_DIR / "output"
RESULTS_PATH = OUTPUT_DIR / "results.json"
ERRORS_PATH = OUTPUT_DIR / "errors.log"


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

def load_config() -> Dict[str, Any]:
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def fetch_url(url: str, timeout_seconds: int) -> Tuple[str, bool, str]:
Â Â Â Â try:
Â Â Â Â Â Â Â Â response = requests.get(url, timeout=timeout_seconds)
Â Â Â Â Â Â Â Â response.raise_for_status()
Â Â Â Â Â Â Â Â return url, True, response.text[:500]
Â Â Â Â except Exception as e:
Â Â Â Â Â Â Â Â return url, False, str(e)


def main() -> None:
Â Â Â Â setup_logging()
Â Â Â Â logging.info("Starting concurrent fetch job")

Â Â Â Â OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
Â Â Â Â RESULTS_PATH.write_text("", encoding="utf-8")
Â Â Â Â ERRORS_PATH.write_text("", encoding="utf-8")

Â Â Â Â cfg = load_config()
Â Â Â Â urls = cfg.get("urls", [])
Â Â Â Â timeout_seconds = int(cfg.get("timeout_seconds", 10))
Â Â Â Â max_workers = int(cfg.get("max_workers", 4))

Â Â Â Â lock = threading.Lock()
Â Â Â Â results: List[Dict[str, Any]] = []
Â Â Â Â successes = 0
Â Â Â Â failures = 0

Â Â Â Â with ThreadPoolExecutor(max_workers=max_workers) as executor:
Â Â Â Â Â Â Â Â futures = {
Â Â Â Â Â Â Â Â Â Â Â Â executor.submit(fetch_url, url, timeout_seconds): url
Â Â Â Â Â Â Â Â Â Â Â Â for url in urls
Â Â Â Â Â Â Â Â }

Â Â Â Â Â Â Â Â for future in as_completed(futures):
Â Â Â Â Â Â Â Â Â Â Â Â url = futures[future]
Â Â Â Â Â Â Â Â Â Â Â Â try:
Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â u, ok, payload = future.result()
Â Â Â Â Â Â Â Â Â Â Â Â except Exception as e:
Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â u, ok, payload = url, False, f"Exception: {e}"

Â Â Â Â Â Â Â Â Â Â Â Â with lock:
Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â if ok:
Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â successes += 1
Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â results.append({"url": u, "ok": ok, "payload": payload})
Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â else:
Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â failures += 1
Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â with ERRORS_PATH.open("a", encoding="utf-8") as ef:
Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â ef.write(f"{u}: {payload}\n")

Â Â Â Â RESULTS_PATH.write_text(json.dumps(results, indent=2), encoding="utf-8")
Â Â Â Â logging.info("Finished concurrent fetch job: %s success, %s failure", successes, failures)


if __name__ == "__main__":
Â Â Â Â main()