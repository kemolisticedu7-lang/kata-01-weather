# Kata 10 — Test-Driven Development (TDD)

## Approach

This feature was implemented using strict TDD:

1. Wrote a failing test
2. Implemented minimal code to pass
3. Refactored while keeping tests green

## TDD Cycles

### Cycle 1 — Low Risk
- Test: score < 0.3 → "low"
- Implemented basic classification

### Cycle 2 — Medium Risk
- Test: score between 0.3 and 0.7 → "medium"
- Extended logic

### Cycle 3 — High Risk
- Test: score ≥ 0.7 → "high"
- Completed classification logic

## Result

All tests pass:

```bash
pytest kata-10/test_report_utils.py

Key Learning

TDD helped ensure:
- correctness from the start
- safe refactoring
- clear, testable design
