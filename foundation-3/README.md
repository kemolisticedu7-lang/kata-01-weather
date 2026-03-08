# Foundation 3 – Flight Delay Data Pipeline

## Overview
This project builds a small MVP data pipeline for processing airline flight delay data.  
The pipeline demonstrates three stages: data acquisition, data transformation, and pipeline integration.

The goal is to show a working implementation of a data processing architecture while understanding the trade-offs involved in implementation.

---

## MVP Iteration 1 – Data Acquisition

The acquisition stage reads raw flight delay data from a CSV dataset.

Script:
src/acquire_data.py

This script:
- Loads the dataset
- Parses the CSV file
- Returns rows as Python dictionaries

Example run:

python3 foundation-3/src/acquire_data.py

Output:

Rows loaded: 10
Sample row: {'FlightDate': '2023-01-01', 'Carrier': 'AA', 'Origin': 'DFW', 'Dest': 'LAX', 'DepDelay': '5'}
---

## MVP Iteration 2 – Data Transformation

The transformation stage cleans the dataset and prepares it for analysis.

Script:
src/transform_data.py
Transformations performed:

- Remove rows with missing delay values
- Convert delay values to numeric format
- Save cleaned data to:
data/transformed/flights_cleaned.csv

Example run:

python3 foundation-3/src/transform_data.py

Output:

Rows after cleaning: 9
---

## MVP Iteration 3 – Pipeline Integration

The pipeline script connects acquisition and transformation.

Script:
src/run_pipeline.py
Run pipeline:

python3 foundation-3/src/run_pipeline.py

Output:

Starting pipeline…
Acquired rows: 10
Transformed rows: 9
Pipeline completed successfully.
---

## Logging and Observability

The pipeline prints clear execution messages for each stage so users can track progress and detect failures.

Future improvements would include:
- structured logging
- pipeline metrics
- automated monitoring