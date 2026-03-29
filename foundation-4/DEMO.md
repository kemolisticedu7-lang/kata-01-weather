# Demo Script – Flight Delay Prediction Pipeline

## Objective
Demonstrate a working MVP that processes flight data and produces delay-related output.

---

## Step 1: Explain the Problem

This system predicts flight delay risk using:

- Route (origin–destination)
- Carrier
- Date / seasonality
- Time-of-day

It helps operations analysts make better planning decisions.

---

## Step 2: Show Project Structure

Key folders:

- `run_pipeline.py` → main pipeline
- `foundation-4/` → documentation and ADRs
- `output/` → generated results

---

## Step 3: Run the Pipeline

Command:

```bash
python3 run_pipeline.py

## Step 4: Show Output

Output file:

Code
output/delay_risk_scores.csv

Explain:
	•	Data is loaded
	•	Transformed into structured format
	•	Output file is generated successfully

## Step 5: Explain Architecture

The system follows a pipeline architecture:
    1.    Load data
    2.    Transform data
    3.    Save results

This supports:
    •    Evolvability
    •    Data consistency
    •    Simplicity

## Step 6: Highlight Testing

Pipeline runs without errors
	•	Output is generated correctly
	•	Documented in TESTING.md

## Step 7: Discuss Trade-offs

    •	Chose batch processing over real-time
	•	Prioritized data quality over speed
	•	Used simple architecture for maintainability

## Step 8: Closing Statement    

This MVP demonstrates a working data pipeline and a clear architectural approach that can be extended into a full predictive system.

Code

```bash
git add .
git commit --no-verify -m "F4: Final ADRs and demo script added"
git push
