# Testing Documentation

## Unit Testing

- Core functions tested:
  - Data loading
  - Data transformation
  - Output writing

## Integration Testing

- Full pipeline tested by running:

python3 run_pipeline.py

- Verified:
  - Data flows correctly from input to output
  - Output file is generated successfully

## Manual Testing

- Confirmed:
  - File `sample_weather.csv` loads correctly
  - Output saved in the `output` folder
  - No runtime errors

## Test Coverage Limitations

- No CI/CD automation implemented
- No edge-case testing for corrupted input files
- Future improvement: add a pytest suite