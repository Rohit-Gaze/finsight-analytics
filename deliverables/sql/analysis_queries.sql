-- FinSight SQL portfolio. TARGET=1 means recorded historical payment difficulties.
-- Table name assumed: application_train.

-- 1. Overall KPIs
SELECT COUNT(*) applications, SUM(TARGET) difficulty_cases, AVG(TARGET) difficulty_rate FROM application_train;

-- 2. Contract type
SELECT NAME_CONTRACT_TYPE, COUNT(*) applications, AVG(TARGET) difficulty_rate FROM application_train GROUP BY 1 ORDER BY 3 DESC;

-- 3. Income type
SELECT NAME_INCOME_TYPE, COUNT(*) applications, AVG(TARGET) difficulty_rate FROM application_train GROUP BY 1 ORDER BY 3 DESC;

-- 4. Education
SELECT NAME_EDUCATION_TYPE, COUNT(*) applications, AVG(TARGET) difficulty_rate FROM application_train GROUP BY 1 ORDER BY 3 DESC;

-- 5. Occupation
SELECT OCCUPATION_TYPE, COUNT(*) applications, AVG(TARGET) difficulty_rate FROM application_train GROUP BY 1 HAVING COUNT(*)>=100 ORDER BY 3 DESC;

-- 6. Family status
SELECT NAME_FAMILY_STATUS, COUNT(*) applications, AVG(TARGET) difficulty_rate FROM application_train GROUP BY 1 ORDER BY 3 DESC;

-- 7. Housing type
SELECT NAME_HOUSING_TYPE, COUNT(*) applications, AVG(TARGET) difficulty_rate FROM application_train GROUP BY 1 ORDER BY 3 DESC;

-- 8. Gender fairness audit only
SELECT CODE_GENDER, COUNT(*) applications, AVG(TARGET) difficulty_rate FROM application_train GROUP BY 1;

-- 9. Organization type
SELECT ORGANIZATION_TYPE, COUNT(*) applications, AVG(TARGET) difficulty_rate FROM application_train GROUP BY 1 HAVING COUNT(*)>=100 ORDER BY 3 DESC;

-- 10. Region rating
SELECT REGION_RATING_CLIENT, COUNT(*) applications, AVG(TARGET) difficulty_rate FROM application_train GROUP BY 1;

-- 11. Weekday
SELECT WEEKDAY_APPR_PROCESS_START, COUNT(*) applications, AVG(TARGET) difficulty_rate FROM application_train GROUP BY 1 ORDER BY 3 DESC;

-- 12. Application hour
SELECT HOUR_APPR_PROCESS_START, COUNT(*) applications, AVG(TARGET) difficulty_rate FROM application_train GROUP BY 1 ORDER BY 1;

-- 13. Median financial values
SELECT MEDIAN(AMT_INCOME_TOTAL), MEDIAN(AMT_CREDIT), MEDIAN(AMT_ANNUITY) FROM application_train;

-- 14. Missing values
SELECT COUNT(*) total_rows, SUM(CASE WHEN OCCUPATION_TYPE IS NULL THEN 1 ELSE 0 END) occupation_missing, SUM(CASE WHEN EXT_SOURCE_1 IS NULL THEN 1 ELSE 0 END) ext1_missing FROM application_train;

-- 15. Credit to income
SELECT AVG(AMT_CREDIT/NULLIF(AMT_INCOME_TOTAL,0)) avg_credit_income FROM application_train;

-- 16. Annuity to income
SELECT AVG(AMT_ANNUITY/NULLIF(AMT_INCOME_TOTAL,0)) avg_annuity_income FROM application_train;

-- 17. Age bands
SELECT CASE WHEN -DAYS_BIRTH/365.25<25 THEN '18-24' WHEN -DAYS_BIRTH/365.25<35 THEN '25-34' WHEN -DAYS_BIRTH/365.25<45 THEN '35-44' WHEN -DAYS_BIRTH/365.25<55 THEN '45-54' WHEN -DAYS_BIRTH/365.25<65 THEN '55-64' ELSE '65+' END age_band, COUNT(*) applications, AVG(TARGET) difficulty_rate FROM application_train GROUP BY 1;

-- 18. Employment bands
SELECT CASE WHEN DAYS_EMPLOYED>-365 THEN '<1 year' WHEN DAYS_EMPLOYED>-1825 THEN '1-5 years' WHEN DAYS_EMPLOYED>-3650 THEN '5-10 years' ELSE '10+ years' END employment_band, COUNT(*) applications, AVG(TARGET) difficulty_rate FROM application_train GROUP BY 1;

-- 19. Income quintiles
WITH x AS (SELECT *, NTILE(5) OVER(ORDER BY AMT_INCOME_TOTAL) q FROM application_train) SELECT q, COUNT(*) applications, AVG(TARGET) difficulty_rate FROM x GROUP BY q ORDER BY q;

-- 20. Credit by contract
SELECT NAME_CONTRACT_TYPE, AVG(AMT_CREDIT), MEDIAN(AMT_CREDIT) FROM application_train GROUP BY 1;

-- 21. Annuity by contract
SELECT NAME_CONTRACT_TYPE, AVG(AMT_ANNUITY) FROM application_train GROUP BY 1;

-- 22. Target counts by gender
SELECT CODE_GENDER, SUM(TARGET), COUNT(*) FROM application_train GROUP BY 1;

-- 23. External score averages
SELECT AVG(EXT_SOURCE_1), AVG(EXT_SOURCE_2), AVG(EXT_SOURCE_3) FROM application_train;

-- 24. Negative value checks
SELECT SUM(CASE WHEN AMT_INCOME_TOTAL<0 THEN 1 ELSE 0 END), SUM(CASE WHEN AMT_CREDIT<0 THEN 1 ELSE 0 END) FROM application_train;

-- 25. Duplicate IDs
SELECT SK_ID_CURR, COUNT(*) FROM application_train GROUP BY 1 HAVING COUNT(*)>1;

-- 26. Contract and weekday
SELECT NAME_CONTRACT_TYPE, WEEKDAY_APPR_PROCESS_START, COUNT(*), AVG(TARGET) FROM application_train GROUP BY 1,2 HAVING COUNT(*)>=100;

-- 27. Income type and education
SELECT NAME_INCOME_TYPE, NAME_EDUCATION_TYPE, COUNT(*), AVG(TARGET) FROM application_train GROUP BY 1,2 HAVING COUNT(*)>=100;

-- 28. Region by contract
SELECT NAME_CONTRACT_TYPE, REGION_RATING_CLIENT, COUNT(*), AVG(TARGET) FROM application_train GROUP BY 1,2;

-- 29. Weekday and hour
SELECT WEEKDAY_APPR_PROCESS_START, HOUR_APPR_PROCESS_START, COUNT(*), AVG(TARGET) FROM application_train GROUP BY 1,2;

-- 30. Segment size check
SELECT NAME_CONTRACT_TYPE, COUNT(*) FROM application_train GROUP BY 1 HAVING COUNT(*)>=500;
