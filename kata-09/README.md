# Kata 9 — Integration Testing

## Overview
This kata demonstrates integration testing for a simple flight delay pipeline.

The pipeline:
- reads flight records from a CSV file
- stores them in SQLite
- generates a summary report by carrier

The integration test verifies the full end-to-end flow from input file to database to output report.

## Files
- `pipeline.py` — runs the pipeline
- `test_integration_pipeline.py` — integration test
- `README.md` — documentation

## How to Run the Test

```bash
pytest kata-09/test_integration_pipeline.py -q

## What the Test Verifies
- input CSV is created and read correctly
- SQLite database is created
- all records are inserted into the database
- output report is generated
- output contains expected columns
- test uses realistic data volume (1000 records)

## Test Isolation
The test uses:
- tmp_path for temporary files
- a temporary SQLite database
- a temporary report file

## Realistic Data Volume
The integration test uses 1000 rows to simulate realistic conditions.

## Git Task: Reflog Recovery
For the Git portion of this kata, I practiced recovering lost commits using git reflog.

Steps performed:
1. Created several commits for kata 9
2. Intentionally ran:

Bash
git reset --hard HEAD~3

3. Used:

Bash
git reflog
to find the lost commit history

4. Recovered the work using

Bash
git reset --hard <commit-hash>
This demonstrated how reflog can recover work after an accidental hard reset.

Stretch
A future improvement would be to add GitHub Actions so integration tests run automatically on push and pull request.
