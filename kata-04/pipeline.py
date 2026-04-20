import argparse
import csv
import hashlib
import logging
import os
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Generator, Iterable, Optional, Tuple


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
DB_PATH = OUTPUT_DIR / "pipeline.db"
REPORT_PATH = OUTPUT_DIR / "report.md"
LOG_PATH = OUTPUT_DIR / "pipeline.log"


# ---------- Setup logging ----------
def setup_logging() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_PATH, mode="a", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


# ---------- Data model ----------
@dataclass(frozen=True)
class Record:
    # Example fields (you will map these to your CSV columns)
    # Update these names/types based on your actual CSV.
    record_id: str
    name: str
    amount: float
    event_date: str  # ISO string YYYY-MM-DD
    source_file: str
    row_num: int


# ---------- Extract (generator) ----------
def extract_csv_rows(csv_path: Path) -> Generator[Tuple[Dict[str, str], int], None, None]:
    """
    Yields (row_dict, row_number) for memory-efficient processing.
    """
    with csv_path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=2):  # header is line 1
            yield row, idx


def extract_all(data_dir: Path) -> Generator[Tuple[Dict[str, str], int, str], None, None]:
    """
    Yields (row_dict, row_number, source_filename) across all CSVs.
    """
    for csv_path in sorted(data_dir.glob("*.csv")):
        for row, row_num in extract_csv_rows(csv_path):
            yield row, row_num, csv_path.name


# ---------- Validate + Transform ----------
def parse_float(value: str) -> Optional[float]:
    try:
        v = float(value)
        return v
    except Exception:
        return None


def normalize_date(value: str) -> Optional[str]:
    """
    Accepts dates like '2026-02-22' or '02/22/2026' and converts to ISO.
    Adjust formats as needed for your dataset.
    """
    value = (value or "").strip()
    if not value:
        return None

    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m-%d-%Y"):
        try:
            return datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            pass
    return None


def make_stable_id(row: Dict[str, str], source_file: str, row_num: int) -> str:
    """
    Generates a deterministic ID when the CSV does not have a reliable one.
    """
    payload = f"{source_file}:{row_num}:{sorted(row.items())}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:16]


def validate_and_transform(
    row: Dict[str, str],
    row_num: int,
    source_file: str
) -> Optional[Record]:
    """
    Returns Record if valid, else logs and returns None (reject malformed).
    Update the field mapping based on your CSV headers.
    """
    # ---- CHANGE THESE to match your CSV headers ----
    name = (row.get("name") or row.get("Name") or "").strip()
    amount_raw = (row.get("amount") or row.get("Amount") or "").strip()
    date_raw = (row.get("date") or row.get("Date") or row.get("event_date") or "").strip()
    record_id = (row.get("id") or row.get("ID") or "").strip()
    # -----------------------------------------------

    if not record_id:
        record_id = make_stable_id(row, source_file, row_num)

    if not name:
        logging.warning(f"Reject row {source_file}:{row_num} -> missing name")
        return None

    amount = parse_float(amount_raw)
    if amount is None:
        logging.warning(f"Reject row {source_file}:{row_num} -> bad amount '{amount_raw}'")
        return None

    event_date = normalize_date(date_raw)
    if event_date is None:
        logging.warning(f"Reject row {source_file}:{row_num} -> bad date '{date_raw}'")
        return None

    return Record(
        record_id=record_id,
        name=name,
        amount=amount,
        event_date=event_date,
        source_file=source_file,
        row_num=row_num,
    )


def transform(
    extracted: Iterable[Tuple[Dict[str, str], int, str]]
) -> Generator[Record, None, None]:
    for row, row_num, source_file in extracted:
        rec = validate_and_transform(row, row_num, source_file)
        if rec:
            yield rec


# ---------- Load (SQLite) ----------
def connect_db(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS records (
            record_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            event_date TEXT NOT NULL,
            source_file TEXT NOT NULL,
            row_num INTEGER NOT NULL
        );
    """)
    conn.commit()


def make_idempotent(conn: sqlite3.Connection) -> None:
    """
    Idempotent approach: clear table before load.
    Alternative: UPSERT by primary key.
    """
    conn.execute("DELETE FROM records;")
    conn.commit()


def load_records(conn: sqlite3.Connection, records: Iterable[Record], dry_run: bool = False) -> int:
    """
    Inserts records. Uses INSERT OR REPLACE for idempotency safety as well.
    """
    count = 0
    if dry_run:
        for _ in records:
            count += 1
        return count

    cur = conn.cursor()
    for r in records:
        cur.execute(
            """
            INSERT OR REPLACE INTO records (record_id, name, amount, event_date, source_file, row_num)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (r.record_id, r.name, r.amount, r.event_date, r.source_file, r.row_num),
        )
        count += 1
        if count % 1000 == 0:
            conn.commit()
    conn.commit()
    return count


# ---------- Report (Markdown) ----------
def generate_report(conn: sqlite3.Connection, out_path: Path, dry_run: bool, inserted: int) -> None:
    now = datetime.now().isoformat(timespec="seconds")
    if dry_run:
        content = f"""# Kata 4 Report (DRY RUN)

- Run time: {now}
- Would insert: **{inserted}** rows
- Database changes: **none** (dry-run)

"""
        out_path.write_text(content, encoding="utf-8")
        return

    total = conn.execute("SELECT COUNT(*) FROM records;").fetchone()[0]
    stats = conn.execute("SELECT MIN(amount), AVG(amount), MAX(amount) FROM records;").fetchone()
    min_amt, avg_amt, max_amt = stats

    content = f"""# Kata 4 Report

- Run time: {now}
- Rows inserted this run: **{inserted}**
- Total rows in database: **{total}**

## Amount statistics
- Min: {min_amt}
- Avg: {avg_amt}
- Max: {max_amt}

## Notes
- Validation rejects are logged to `{LOG_PATH.name}`.
- Pipeline is idempotent (table cleared then reloaded).

"""
    out_path.write_text(content, encoding="utf-8")


# ---------- Main orchestration ----------
def run_pipeline(dry_run: bool) -> None:
    setup_logging()

    if not DATA_DIR.exists():
        logging.error(f"Missing data directory: {DATA_DIR}")
        logging.error("Put one or more CSV files in kata-04/data/")
        return

    extracted = extract_all(DATA_DIR)
    transformed = transform(extracted)

    if dry_run:
        inserted = load_records(conn=None, records=transformed, dry_run=True)  # type: ignore
        generate_report(conn=None, out_path=REPORT_PATH, dry_run=True, inserted=inserted)  # type: ignore
        logging.info(f"DRY RUN complete. Would insert {inserted} rows.")
        logging.info(f"Report written to {REPORT_PATH}")
        return

    conn = connect_db(DB_PATH)
    try:
        init_schema(conn)
        make_idempotent(conn)
        inserted = load_records(conn, transformed, dry_run=False)
        generate_report(conn, REPORT_PATH, dry_run=False, inserted=inserted)
        logging.info(f"Loaded {inserted} records into {DB_PATH}")
        logging.info(f"Report written to {REPORT_PATH}")
    finally:
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Kata 4 - Data Transformation Pipeline")
    parser.add_argument("--dry-run", action="store_true", help="Process data but do not write to database")
    args = parser.parse_args()
    run_pipeline(dry_run=args.dry_run)


if __name__ == "__main__":
    main()