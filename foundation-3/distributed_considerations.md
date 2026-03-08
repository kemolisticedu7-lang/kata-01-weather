# Distributed System Considerations

## Current Architecture

The current pipeline is a **monolithic pipeline** executed on a single machine.

All stages run sequentially.

---

## Distribution Decision

The pipeline was intentionally kept monolithic because:

- The dataset is small
- Complexity of distributed systems is unnecessary at this stage
- Development speed is more important for an MVP

---

## Potential Distributed Architecture

If the system scaled to large datasets, the architecture could evolve into a distributed pipeline.

Possible improvements include:

- Distributed processing using Spark or Dask
- Message queues for data ingestion
- Separate services for acquisition and transformation

---

## Data Ownership

Currently, all data is stored locally.

Raw data is stored in:

data/raw
Cleaned data is stored in:

data/transformed
In a distributed architecture, data ownership would likely move to centralized storage such as cloud object storage.