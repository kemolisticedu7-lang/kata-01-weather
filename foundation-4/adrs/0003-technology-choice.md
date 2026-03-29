# ADR 0003: Technology Choice

## Status
Accepted

## Context
The system requires a technology stack for:

- Data processing
- File handling
- Pipeline execution

The technology should:
- Be easy to use and understand
- Support rapid development
- Be suitable for data pipelines

## Decision
I selected **Python** as the primary implementation language.

## Consequences

### Positive
- Simple and readable syntax
- Strong support for data processing
- Large ecosystem (pandas, csv, etc.)
- Easy to prototype and debug

### Negative
- Slower performance compared to compiled languages
- Not ideal for very large-scale distributed systems
- Requires careful structure to maintain code quality

## Trade-off
I prioritized **developer productivity and flexibility** over raw performance.