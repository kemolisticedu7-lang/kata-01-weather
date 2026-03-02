import json
import logging
logging.info("Starting concurrent fetch job")
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Paths
from typing import Any, Dict, List, Tuples
import requests


BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"
OUTPUT_DIR = BASE_DIR / "output"
RESULTS_PATH = OUTPUT_DIR / "results.jsonl"
ERRORS_PATH = OUTPUT_DIR / "errors.log"


def setup_logging() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()],
    )


def load_config() -> Dict[str, Any]:
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def fetch_url(url: str, timeout_seconds: int) -> Tuple[str, bool, Any]:
    """
    Returns (url, success, data_or_error)
    """
    try:
        r = requests.get(url, timeout=timeout_seconds)
        r.raise_for_status()

        # Try JSON first, fall back to text
        try:
            return url, True, r.json()
        except Exception:
            return url, True, r.text

    except Exception as e:
        return url, False, str(e)


def main() -> None:
    setup_logging()
    cfg = load_config()

    urls: List[str] = cfg.get("urls", [])
    max_workers: int = int(cfg.get("thread_pool_size", 8))
    timeout_seconds: int = int(cfg.get("timeout_seconds", 10))

    if not urls:
        logging.error("No URLs found in config.json")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Thread-safe file writing
    lock = threading.Lock()

    # Clear output files each run (idempotent-ish)
    RESULTS_PATH.write_text("", encoding="utf-8")
    ERRORS_PATH.write_text("", encoding="utf-8")

    start = datetime.now()

    logging.info(f"Fetching {len(urls)} URLs with {max_workers} threads (timeout={timeout_seconds}s)")

    successes = 0
    failures = 0

RESULTS_PATH.write_text("", encoding="utf-8")
ERRORS_PATH.write_text("", encoding="utf-8")

with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(fetch_url, url, timeout_seconds): url for url in urls}

        for future in as_completed(futures):
            url = futures[future]
            try:
                u, ok, payload = future.result()
           except Exception as e:
                u, ok, payload = url, false, f"Exception: {e}"
            with lock:
                if ok:
                    successes += 1
                    record = {"url": u, "ok": True, "data": payload}
                    with RESULTS_PATH.open("a", encoding="utf-8") as rf:
                        rf.write(json.dumps(record) + "\n")
                else:
                    failures += 1
                    with ERRORS_PATH.open("a", encoding="utf-8") as ef:
                        ef.write(f"{u} -> {payload}\n")

            logging.info(f"[{'OK' if ok else 'FAIL'}] URL: {url}")

    elapsed = (datetime.now() - start).total_seconds()
    logging.info(f"Done. Success={successes}, Fail={failures}, Time={elapsed:.2f}s")
    logging.info(f"Results: {RESULTS_PATH}")
    logging.info(f"Errors:  {ERRORS_PATH}")


if __name__ == "__main__":
    main()