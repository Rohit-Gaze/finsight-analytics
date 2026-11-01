# Power BI Desktop — Final Dashboard Assembly

A native `.pbix` file must be created and saved from Power BI Desktop. This package includes the measures, data model plan, verified reference metrics, and a self-contained interactive HTML dashboard. The HTML dashboard is not a `.pbix` substitute.

## Load data
1. Open Power BI Desktop → Get Data → Text/CSV.
2. Select `data/application_train.csv`.
3. Load the table and rename it `application_train`.
4. Set `TARGET` to Whole Number; amount columns to Decimal Number; IDs and categorical codes to appropriate types.
5. Add measures from `measures.dax`.

## Page 1 — Executive Overview
- KPI cards: Applications, Payment Difficulty Cases, Payment Difficulty Rate, Median Income, Median Credit, Median Annuity.
- Donut: TARGET split.
- Bar: historical payment-difficulty rate by contract type.
- Add application count to tooltips.

## Page 2 — Portfolio Segmentation
- Bar charts by income type, education, occupation and age band.
- Use application count in tooltips; avoid interpreting groups with low volume.
- Add slicers for contract type and income type.

## Page 3 — Affordability
- Scatter plot: AMT_INCOME_TOTAL vs AMT_CREDIT (use aggregation or a sample to avoid overplotting).
- Create calculated columns or measures for credit/income and annuity/income ratios.
- Include distributions and missingness caveats.

## Page 4 — Data Quality & Governance
- Import `deliverables/reports/missingness_profile.csv`.
- Show top missing fields and a table of data definitions.
- Add a note: TARGET=1 is recorded historical payment difficulty, not necessarily legal default.

## Validation
Compare Power BI card values with `deliverables/reports/executive_kpis.csv`. Overall expected values:
- Applications: 307,511
- TARGET=1: 24,825
- TARGET=0: 282,686
- TARGET rate: approximately 8.07%

Financial amounts are dataset currency units, not assumed INR. This is descriptive analysis, not a causal model or production underwriting system.
