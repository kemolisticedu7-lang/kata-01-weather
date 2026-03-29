# ADR 0001: Data Source Selection

## Status
Accepted

## Context
The system requires a reliable dataset to analyze and predict flight delays using pre-departure information. The dataset must:

- Be publicly accessible
- Contain consistent fields across time
- Include relevant features such as carrier, route, and timing
- Support reproducibility for batch processing

## Decision
I selected the **Bureau of Transportation Statistics (BTS) Airline On-Time Performance dataset**, along with the **Carrier Lookup dataset**.

## Consequences

### Positive
- High-quality, real-world dataset
- Consistent structure across months
- Rich features for delay analysis
- Publicly accessible and reproducible

### Negative
- Large dataset size (scalability concern)
- Some delay-cause fields are incomplete or inconsistent
- Requires preprocessing and cleaning before use

## Trade-off
I prioritized **data quality and availability** over simplicity of use.