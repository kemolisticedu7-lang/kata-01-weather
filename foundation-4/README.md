# Foundation 4 – Flight Delay Prediction Pipeline (MVP)

## Problem
The system predicts the likelihood of flight delays using pre-departure factors:

- Route (Origin–Destination)
- Carrier
- Date / Seasonality
- Time-of-day

This helps operations analysts anticipate delays and improve planning decisions such as staffing and scheduling buffers.

---

## System Overview

This project implements a **batch data pipeline** that:

1. Loads flight data
2. Cleans and transforms it
3. Generates delay-related features
4. Outputs a dataset for delay risk analysis

The architecture follows a **pipeline (ETL-style) modular design**.

---

## How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt