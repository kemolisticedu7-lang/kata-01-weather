import json
import math
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import Manager


BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"
OUT_DIR = BASE_DIR / "output"
RESULT_PATH = OUT_DIR / "results.json"
ERROR_PATH = OUT_DIR / "errors.log"


@dataclass
class ChunkResult:
    chunk_index: int
    count: int
    mean: float
    stddev: float
    min_val: float
    max_val: float


def load_config() -> Dict[str, Any]:
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def ensure_output_dir() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)


def reset_outputs() -> None:
    RESULT_PATH.write_text("", encoding="utf-8")
    ERROR_PATH.write_text("", encoding="utf-8")


def generate_dataset(num_records: int) -> List[float]:
    # Simulated “large dataset”: deterministic numeric signal
    # (keeps it repeatable for grading / bisect)
    data = []
    for i in range(num_records):
        # Some CPU-ish math
        x = (i % 1000) / 10.0
        v = math.sin(x) * math.cos(x / 2.0) + (x ** 2) * 0.0001
        data.append(v)
    return data


def chunkify(data: List[float], chunk_size: int) -> List[Tuple[int, List[float]]]:
    chunks = []
    idx = 0
    for start in range(0, len(data), chunk_size):
        chunks.append((idx, data[start : start + chunk_size]))
        idx += 1
    return chunks


def process_chunk(args):
    chunk_index, chunk, simulate_bug, shared, lock = args

    try:
        # Intentional bug for testing / bisect
        if simulate_bug and chunk_index == 2:
            raise RuntimeError("Intentional bug: chunk 2 fails")

        n = len(chunk)

        if n == 0:
            with lock:
                shared["ok"] = int(shared.get("ok", 0)) + 1
                shared["notes"].append(f"chunk {chunk_index}: empty but ok")
            return ChunkResult(chunk_index, 0, 0.0, 0.0, 0.0, 0.0)

        s = 0.0
        s2 = 0.0
        mn = chunk[0]
        mx = chunk[0]

        for v in chunk:
            s += v
            s2 += v * v
            if v < mn:
                mn = v
            if v > mx:
                mx = v

        mean = s / n
        variance = (s2 / n) - (mean * mean)
        stddev = math.sqrt(max(variance, 0.0))

        with lock:
            shared["ok"] = int(shared.get("ok", 0)) + 1

        return ChunkResult(chunk_index, n, mean, stddev, mn, mx)

    except Exception as e:
        with lock:
            shared["fail"] = int(shared.get("fail", 0)) + 1
            shared["notes"].append(f"chunk {chunk_index} failed: {e}")
        raise

def combine_results(results: List[ChunkResult]) -> Dict[str, Any]:
    # Combine chunk stats into overall stats using weighted approach
    total_count = sum(r.count for r in results)
    if total_count == 0:
        return {"count": 0, "mean": 0.0, "stddev": 0.0, "min": 0.0, "max": 0.0}

    overall_min = min(r.min_val for r in results if r.count > 0)
    overall_max = max(r.max_val for r in results if r.count > 0)

    # Weighted mean
    weighted_sum = sum(r.mean * r.count for r in results)
    overall_mean = weighted_sum / total_count

    # Combine variance (approx) from chunk stddev + chunk mean differences
    # Var(total) = sum_i [ n_i*(var_i + (mean_i - mean_total)^2 ) ] / N
    accum = 0.0
    for r in results:
        var_i = r.stddev * r.stddev
        accum += r.count * (var_i + (r.mean - overall_mean) ** 2)
    overall_var = accum / total_count
    overall_stddev = math.sqrt(overall_var) if overall_var > 0 else 0.0

    return {
        "count": total_count,
        "mean": overall_mean,
        "stddev": overall_stddev,
        "min": overall_min,
        "max": overall_max,
    }


def main() -> None:
    ensure_output_dir()
    reset_outputs()

    cfg = load_config()
    simulate_bug = cfg.get("simulate_bug", False)
    num_records = int(cfg.get("num_records", 200000))
    chunk_size = int(cfg.get("chunk_size", 20000))
    max_workers = int(cfg.get("max_workers", os.cpu_count() or 4))
    simulate_bug = bool(cfg.get("simulate_bug", False))

    print(f"[INFO] Generating dataset: {num_records} records...")
    data = generate_dataset(num_records)
    chunks = chunkify(data, chunk_size)
    print("[DEBUG] first chunk indexes:", [c[0] for c in chunks[:5]])
    total_chunks = len(chunks)
    print(f"[INFO] Split into {total_chunks} chunks (chunk_size={chunk_size})")
    print(f"[INFO] Processing with ProcessPoolExecutor(max_workers={max_workers})")
   

    started = datetime.now()
    completed = 0
    successes: List[ChunkResult] = []

    manager = Manager()
    shared = manager.dict()
    shared["ok"] = 0
    shared["fail"] = 0
    shared["notes"] = manager.list()
    lock = manager.Lock()

    with ProcessPoolExecutor(max_workers=max_workers) as ex:
        futures = {
            ex.submit(
                process_chunk,
                (chunk_index, chunk, simulate_bug, shared, lock)
        ): chunk_index
        for (chunk_index, chunk) in chunks
    }

    for fut in as_completed(futures):
        chunk_index = futures[fut]
        try:
            res = fut.result()
            successes.append(res)
            completed += 1
            print(f"[OK] chunk {chunk_index} done ({completed}/{total_chunks})")

        except Exception as e:
            completed += 1
            msg = f"[FAIL] chunk {chunk_index} ({completed}/{total_chunks}): {e}\n"
            print(msg.strip())
            with ERROR_PATH.open("a", encoding="utf-8") as ef:
                ef.write(msg)

    successes.sort(key=lambda r: r.chunk_index)
    summary = combine_results(successes)

    elapsed = (datetime.now() - started).total_seconds()

    output = {
        "run_time": started.isoformat(),
        "elapsed_seconds": elapsed,
        "num_records": num_records,
        "chunk_size": chunk_size,
        "max_workers": max_workers,
        "chunks_total": total_chunks,
        "chunks_succeeded": len(successes),
        "summary": summary,
    }

    RESULT_PATH.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"[INFO] Manager totals: ok={shared['ok']} fail={shared['fail']}")
    print("[INFO] Sample notes:", list(shared["notes"])[:5])


if __name__ == "__main__":
    main()