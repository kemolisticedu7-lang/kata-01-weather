import csv
import sqlite3
from pathlib import Path


def run_pipeline(input_csv: Path, db_path: Path, report_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS flights (
            date TEXT,
            carrier TEXT,
            origin TEXT,
            dest TEXT,
            dep_delay INTEGER
        )
    """)

    with input_csv.open("r", newline="") as f:
        reader = csv.DictReader(f)
        rows = [
            (
                row["date"],
                row["carrier"],
                row["origin"],
                row["dest"],
                int(row["dep_delay"]),
            )
            for row in reader
        ]

    cur.executemany(
        "INSERT INTO flights (date, carrier, origin, dest, dep_delay) VALUES (?, ?, ?, ?, ?)",
        rows,
    )
    conn.commit()

    cur.execute("""
        SELECT carrier,
               COUNT(*) AS flight_count,
               AVG(CASE WHEN dep_delay > 15 THEN 1.0 ELSE 0.0 END) AS delay_rate
        FROM flights
        GROUP BY carrier
        ORDER BY carrier
    """)
    results = cur.fetchall()
    conn.close()

    with report_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["carrier", "flight_count", "delay_rate"])
        writer.writeheader()
        for carrier, flight_count, delay_rate in results:
            writer.writerow({
                "carrier": carrier,
                "flight_count": flight_count,
                "delay_rate": round(delay_rate, 3),
            })