# Methodology and assumptions

1. Load the application-level CSV and inspect the target and numeric financial fields.
2. Calculate row counts, target counts, target rate, and median financial amounts.
3. Profile missingness at column level.
4. Compare historical target rates across contract, income, education, occupation, family, housing, age, and income segments.
5. Apply a minimum segment size of 100 in the generated segment summaries to reduce unstable small-group comparisons.
6. Create visual summaries and a Power BI measure/dashboard plan.

## Definitions
- Applications: one row per application record.
- Payment difficulty case: `TARGET=1`.
- Other target case: `TARGET=0`.
- Payment difficulty rate: mean of the binary TARGET field.
- Age: `-DAYS_BIRTH / 365.25`, an approximation.
- Income bands: quintiles based on application income rank.

## Limitations
This is a historical observational dataset. Segment differences do not establish causation. Missingness may be informative. The analysis does not train or validate a prediction model, estimate credit losses, or establish regulatory compliance. Validate business definitions with domain stakeholders before operational use.
