# Risk Identification

## Technical Risks

The pipeline relies on correct file paths and CSV formatting.

If the dataset structure changes, the scripts may fail or produce incorrect results.

Another risk is dependency management if the pipeline expands to include additional libraries.

---

## Data Risks

Data quality is a major risk.

Possible issues include:

- Missing values
- Incorrect data formats
- Inconsistent airline codes

The current pipeline removes rows with missing delay values, but more advanced validation may be needed.

---

## Architectural Risks

The architecture is simple but may not scale well for large datasets.

If the dataset becomes very large, the pipeline would require distributed processing or database integration.

Refactoring would likely be required to support high-volume processing.