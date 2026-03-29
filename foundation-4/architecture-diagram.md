# Architecture Diagram – Flight Delay Prediction Pipeline

## Overview
This diagram represents the batch pipeline architecture used to process flight data and generate delay risk outputs.

---

## Diagram

```mermaid
flowchart LR

A[Raw Data\n(sample_weather.csv)] --> B[Data Loading]

B --> C[Data Transformation]

C --> D[Feature Engineering\n(delay indicators)]

D --> E[Save Results]

E --> F[Output File\noutput/delay_risk_scores.csv]

subgraph Pipeline
B
C
D
E
end

Explanation

The system follows a pipeline (ETL-style) architecture:
    1.    Data Loading
    •    Reads input CSV data
    2.    Data Transformation
    •    Cleans and prepares data
    •    Applies logic for delay indicators
    3.    Feature Engineering
    •    Creates structured fields used for analysis
    4.    Save Results
    •    Writes processed data to output file
    5.    Output
    •    Final dataset stored in the output/ folder

⸻

Design Rationale

This architecture was chosen because:
    •    It supports evolvability (easy to modify steps)
    •    It ensures data consistency (controlled transformations)
    •    It is simple and appropriate for batch processing

⸻

Notes
    •    This is a modular monolith pipeline
    •    Each stage has a single responsibility
    •    Data flows sequentially from input to output