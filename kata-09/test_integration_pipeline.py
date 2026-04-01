import csv
import sqlite3
from pathlib import Path

from pipeline import run_pipeline


def write_sample_csv(path: Path, rows: int) -> None:
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["date", "carrier", "origin", "dest", "dep_delay"]
        )
        writer.writeheader()
        for i in range(rows):
            writer.writerow({
                "date": f"2026-01-{(i % 28) + 1:02d}",
                "carrier": "AA" if i % 2 == 0 else "DL",
                "origin": "DFW",
                "dest": "ORD",
                "dep_delay": 20 if i % 3 == 0 else 5,
            })


def test_pipeline_end_to_end(tmp_path):
    input_csv = tmp_path / "flights.csv"
    db_path = tmp_path / "flights.db"
    report_path = tmp_path / "report.csv"

    write_sample_csv(input_csv, rows=1000)

    run_pipeline(input_csv=input_csv, db_path=db_path, report_path=report_path)

    assert db_path.exists()
    assert report_path.exists()

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM flights")
    count = cur.fetchone()[0]
    conn.close()

    assert count == 1000

    with report_path.open("r", newline="") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 2
    assert "carrier" in rows[0]
    assert "flight_count" in rows[0]
    assert "delay_rate" in rows[0]