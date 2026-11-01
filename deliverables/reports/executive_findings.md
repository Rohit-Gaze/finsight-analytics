# FinSight Analytics — Executive Findings

## Executive summary
- **Applications:** 307,511
- **Recorded payment-difficulty cases:** 24,825
- **Other target cases:** 282,686
- **Historical payment-difficulty rate:** 8.07%
- **Median income:** 147,150 dataset currency units
- **Median credit:** 513,531 dataset currency units
- **Median annuity:** 24,903 dataset currency units

## Segment observations
These are descriptive differences, not causal explanations. Segment rates are shown with application counts.

- **AGE_BAND:** highest observed segment rate `18-24` = 12.29% (n=12,233); lowest `65+` = 3.66% (n=7,876).
- **INCOME_BAND:** highest observed segment rate `Q2` = 8.75% (n=61,502); lowest `Q5 highest` = 6.79% (n=61,502).
- **NAME_CONTRACT_TYPE:** highest observed segment rate `Cash loans` = 8.35% (n=278,232); lowest `Revolving loans` = 5.48% (n=29,279).
- **NAME_EDUCATION_TYPE:** highest observed segment rate `Lower secondary` = 10.93% (n=3,816); lowest `Academic degree` = 1.83% (n=164).
- **NAME_FAMILY_STATUS:** highest observed segment rate `Civil marriage` = 9.94% (n=29,775); lowest `Widow` = 5.82% (n=16,088).
- **NAME_HOUSING_TYPE:** highest observed segment rate `Rented apartment` = 12.31% (n=4,881); lowest `Office apartment` = 6.57% (n=2,617).
- **NAME_INCOME_TYPE:** highest observed segment rate `Working` = 9.59% (n=158,774); lowest `Pensioner` = 5.39% (n=55,362).
- **OCCUPATION_TYPE:** highest observed segment rate `Low-skill Laborers` = 17.15% (n=2,093); lowest `Accountants` = 4.83% (n=9,813).

## Business implications to investigate
1. **Affordability review:** compare credit-to-income and annuity-to-income ratios against historical payment-difficulty outcomes, while checking for missing and extreme values.
2. **Portfolio monitoring:** track both application volume and outcome rate by product/contract and operational segments; avoid ranking groups using rates alone.
3. **Data quality:** prioritize completeness and definition checks for fields with high missingness before using them in operational reporting.
4. **Validation:** investigate whether observed segment differences persist in newer time periods and after controlling for product mix and other confounders.

## Important limitations
`TARGET=1` denotes recorded payment difficulties according to the dataset definition. It is not necessarily a legal default, loan rejection, or a causal outcome. This project is descriptive; it does not train a predictive model, establish causality, or provide lending policy. Currency amounts are dataset currency units, not assumed INR. Demographic segment comparisons are for cautious audit/context only and must not be used as standalone adverse lending criteria.
