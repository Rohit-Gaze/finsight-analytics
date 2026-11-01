-- FinSight analytical SQL library
-- Load data table `applications` from data/finsight_application_features.csv.
-- Target: payment_difficulty = 1 is the recorded Home Credit target outcome.

-- 01. Executive KPIs
SELECT COUNT(*) AS applications,
       SUM(payment_difficulty) AS payment_difficulty_cases,
       AVG(payment_difficulty * 1.0) AS payment_difficulty_rate,
       AVG(annual_income) AS avg_income,
       AVG(credit_amount) AS avg_credit
FROM applications;

-- 02. Risk by contract type
SELECT contract_type, COUNT(*) AS applications,
       SUM(payment_difficulty) AS cases,
       AVG(payment_difficulty * 1.0) AS difficulty_rate
FROM applications
GROUP BY contract_type
ORDER BY difficulty_rate DESC;

-- 03. Risk by income type
SELECT income_type, COUNT(*) AS applications,
       AVG(payment_difficulty * 1.0) AS difficulty_rate
FROM applications
GROUP BY income_type
HAVING COUNT(*) >= 100
ORDER BY difficulty_rate DESC;

-- 04. Risk by age band
SELECT CASE
         WHEN age_years < 25 THEN '18-24'
         WHEN age_years < 35 THEN '25-34'
         WHEN age_years < 45 THEN '35-44'
         WHEN age_years < 55 THEN '45-54'
         WHEN age_years < 65 THEN '55-64'
         ELSE '65+'
       END AS age_band,
       COUNT(*) AS applications,
       AVG(payment_difficulty * 1.0) AS difficulty_rate
FROM applications
GROUP BY age_band
ORDER BY age_band;

-- 05. Credit-to-income bands
SELECT CASE
         WHEN credit_to_income < 2 THEN '<2x'
         WHEN credit_to_income < 4 THEN '2x-4x'
         WHEN credit_to_income < 6 THEN '4x-6x'
         ELSE '6x+'
       END AS credit_income_band,
       COUNT(*) AS applications,
       AVG(payment_difficulty * 1.0) AS difficulty_rate
FROM applications
WHERE credit_to_income IS NOT NULL
GROUP BY credit_income_band
ORDER BY credit_income_band;

-- 06. External score comparison (descriptive association only)
SELECT
  CASE WHEN external_score_avg < 0.25 THEN 'Low'
       WHEN external_score_avg < 0.50 THEN 'Medium-low'
       WHEN external_score_avg < 0.75 THEN 'Medium-high'
       ELSE 'High' END AS score_band,
  COUNT(*) AS applications,
  AVG(payment_difficulty * 1.0) AS difficulty_rate
FROM applications
WHERE external_score_avg IS NOT NULL
GROUP BY score_band
ORDER BY score_band;

-- 07. Occupation segments with minimum sample size
SELECT occupation_type, COUNT(*) AS applications,
       AVG(payment_difficulty * 1.0) AS difficulty_rate
FROM applications
WHERE occupation_type IS NOT NULL
GROUP BY occupation_type
HAVING COUNT(*) >= 500
ORDER BY difficulty_rate DESC;

-- 08. Monthly-style application-hour pattern
SELECT bureau_queries_year, COUNT(*) AS applications,
       AVG(payment_difficulty * 1.0) AS difficulty_rate
FROM applications
GROUP BY bureau_queries_year
ORDER BY bureau_queries_year;

-- 09. Rank contract types by observed rate
WITH contract_risk AS (
  SELECT contract_type, COUNT(*) AS applications,
         AVG(payment_difficulty * 1.0) AS difficulty_rate
  FROM applications GROUP BY contract_type
)
SELECT *, DENSE_RANK() OVER (ORDER BY difficulty_rate DESC) AS risk_rank
FROM contract_risk;

-- 10. Customer-level affordability indicators
SELECT application_id, annual_income, credit_amount, annuity_amount,
       credit_to_income, annuity_to_income, payment_difficulty
FROM applications
ORDER BY annuity_to_income DESC
LIMIT 100;

-- 11. Missing external score patterns
SELECT
  CASE WHEN external_score_1 IS NULL THEN 1 ELSE 0 END AS missing_score_1,
  CASE WHEN external_score_2 IS NULL THEN 1 ELSE 0 END AS missing_score_2,
  CASE WHEN external_score_3 IS NULL THEN 1 ELSE 0 END AS missing_score_3,
  COUNT(*) AS applications,
  AVG(payment_difficulty * 1.0) AS difficulty_rate
FROM applications
GROUP BY missing_score_1, missing_score_2, missing_score_3
ORDER BY applications DESC;

-- 12. Segment contribution: cases and share of all cases
WITH segments AS (
  SELECT income_type, COUNT(*) AS applications,
         SUM(payment_difficulty) AS cases
  FROM applications GROUP BY income_type
)
SELECT income_type, applications, cases,
       cases * 1.0 / NULLIF(SUM(cases) OVER (), 0) AS share_of_difficulty_cases
FROM segments
ORDER BY cases DESC;
