# ADR 0002: Architecture Style Selection

## Status
Accepted

## Context
The system must process structured flight data through multiple stages:

- Ingestion
- Validation
- Transformation
- Output generation

The architecture must support:
- Evolvability
- Data consistency
- Simplicity of implementation

## Decision
I chose a **Pipeline Architecture (Batch ETL)** implemented as a **modular monolith**.

## Consequences

### Positive
- Clear separation of stages
- Easy to extend and modify
- Simple deployment (single system)
- Matches batch nature of BTS data

### Negative
- No real-time processing capability
- Limited scalability compared to distributed systems
- Tight coupling between stages

## Trade-off
I prioritized **simplicity and evolvability** over real-time performance and distributed scalability.