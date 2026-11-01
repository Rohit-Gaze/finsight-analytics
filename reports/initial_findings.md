# FinSight — Initial Data Findings

## Project scope
This analysis uses the Home Credit Default Risk `application_train.csv` file. The target is `TARGET`:
- `0`: application did not have the recorded payment-difficulty outcome.
- `1`: application had the recorded payment-difficulty outcome.

**Important:** This is an application-level target label. It should not be casually described as a confirmed loan default, approval decision, or causal risk factor.

## Dataset profile
- Rows: 307,511
- Source columns: 122
- Payment-difficulty cases: 24,825
- Other cases: 282,686
- Overall payment-difficulty rate: 8.07%
- Duplicate application IDs: 0

## Initial descriptive findings
1. Cash-loan applications have a recorded payment-difficulty rate of 8.35%, compared with 5.48% for revolving-loan applications. This is an unadjusted association, not evidence that contract type causes difficulty.
2. The observed rate is 10.14% for records coded M and 7.00% for records coded F. This is descriptive only and should not be used as a standalone lending decision rule.
3. The rate is 10.93% among applicants with lower-secondary education and 5.36% among applicants with higher education. Segment sizes differ; interpret carefully and avoid discriminatory decision use.
4. Median age is 39.1 years in the payment-difficulty group and 43.5 years in the other group.
5. The dataset has substantial missingness in several property-related fields. The highest missing columns include: COMMONAREA_AVG (69.9%), COMMONAREA_MODE (69.9%), COMMONAREA_MEDI (69.9%), NONLIVINGAPARTMENTS_MEDI (69.4%), NONLIVINGAPARTMENTS_MODE (69.4%).

## Analytical limitations
- The dataset is observational and historical.
- The target is not a direct measure of lifetime default or current delinquency.
- Differences between groups are not causal effects.
- Sensitive attributes such as gender and education require fairness review and must not be used as simplistic adverse decision rules.
- This project is for portfolio analytics and learning, not a production credit decision system.

## Next analysis
- Validate data types, missingness, outliers and special sentinel values.
- Examine income, credit, annuity and external-score distributions.
- Build segment tables and confidence intervals.
- Compare findings with multivariate analysis only after checking leakage, fairness and sampling.
