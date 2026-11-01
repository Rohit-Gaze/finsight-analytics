from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

root=Path.cwd()
data=root/'data'/'application_train.csv'
if not data.exists():
    raise FileNotFoundError('Place application_train.csv in the project data folder.')
out=root/'deliverables'
for folder in ('reports','charts','sql','powerbi'):
    (out/folder).mkdir(parents=True,exist_ok=True)

df=pd.read_csv(data)
n=len(df); target=int(df['TARGET'].sum()); rate=target/n
rep=out/'reports'
pd.DataFrame([
    ['Applications',n],['Payment difficulty cases',target],
    ['Other cases',n-target],['Payment difficulty rate',rate],
    ['Median income',df.AMT_INCOME_TOTAL.median()],
    ['Median credit',df.AMT_CREDIT.median()],
    ['Median annuity',df.AMT_ANNUITY.median()]
],columns=['metric','value']).to_csv(rep/'executive_kpis.csv',index=False)

d=df[['TARGET','NAME_CONTRACT_TYPE','NAME_INCOME_TYPE','NAME_EDUCATION_TYPE',
      'OCCUPATION_TYPE','NAME_FAMILY_STATUS','NAME_HOUSING_TYPE',
      'AMT_INCOME_TOTAL','AMT_CREDIT','AMT_ANNUITY','DAYS_BIRTH']].copy()
d['AGE_YEARS']=-d.DAYS_BIRTH/365.25
d['AGE_BAND']=pd.cut(d.AGE_YEARS,[0,25,35,45,55,65,100],
                     labels=['18-24','25-34','35-44','45-54','55-64','65+'])
d['INCOME_BAND']=pd.qcut(d.AMT_INCOME_TOTAL.rank(method='first'),5,
                         labels=['Q1 lowest','Q2','Q3','Q4','Q5 highest'])
segments=['NAME_CONTRACT_TYPE','NAME_INCOME_TYPE','NAME_EDUCATION_TYPE',
          'OCCUPATION_TYPE','NAME_FAMILY_STATUS','NAME_HOUSING_TYPE',
          'AGE_BAND','INCOME_BAND']
for col in segments:
    x=d.groupby(col,dropna=False,observed=False).TARGET.agg(
        applications='size',payment_difficulty_rate='mean').reset_index()
    x=x[x.applications>=100].sort_values('payment_difficulty_rate',ascending=False)
    x.to_csv(rep/('risk_by_'+col.lower()+'.csv'),index=False)
    if len(x):
        fig,ax=plt.subplots(figsize=(9,max(3,len(x)*.38)))
        ax.barh(x[col].astype(str),x.payment_difficulty_rate*100)
        ax.set_xlabel('Historical payment difficulty rate (%)')
        ax.set_title('Payment difficulty by '+col)
        ax.invert_yaxis(); fig.tight_layout()
        fig.savefig(out/'charts'/(col.lower()+'.png'),dpi=150); plt.close(fig)

missing=(df.isna().mean()*100).sort_values(ascending=False).rename('missing_pct').reset_index()
missing.columns=['column','missing_pct']
missing.to_csv(rep/'missingness_profile.csv',index=False)
fig,ax=plt.subplots(figsize=(10,6))
top=missing.head(15).sort_values('missing_pct')
ax.barh(top.column,top.missing_pct); ax.set_xlabel('Missing values (%)')
ax.set_title('15 fields with highest missingness'); fig.tight_layout()
fig.savefig(out/'charts'/'missingness.png',dpi=150); plt.close(fig)

queries=[
('Overall KPIs','SELECT COUNT(*) applications, SUM(TARGET) difficulty_cases, AVG(TARGET) difficulty_rate FROM application_train;'),
('Contract type','SELECT NAME_CONTRACT_TYPE, COUNT(*) applications, AVG(TARGET) difficulty_rate FROM application_train GROUP BY 1 ORDER BY 3 DESC;'),
('Income type','SELECT NAME_INCOME_TYPE, COUNT(*) applications, AVG(TARGET) difficulty_rate FROM application_train GROUP BY 1 ORDER BY 3 DESC;'),
('Education','SELECT NAME_EDUCATION_TYPE, COUNT(*) applications, AVG(TARGET) difficulty_rate FROM application_train GROUP BY 1 ORDER BY 3 DESC;'),
('Occupation','SELECT OCCUPATION_TYPE, COUNT(*) applications, AVG(TARGET) difficulty_rate FROM application_train GROUP BY 1 HAVING COUNT(*)>=100 ORDER BY 3 DESC;'),
('Family status','SELECT NAME_FAMILY_STATUS, COUNT(*) applications, AVG(TARGET) difficulty_rate FROM application_train GROUP BY 1 ORDER BY 3 DESC;'),
('Housing type','SELECT NAME_HOUSING_TYPE, COUNT(*) applications, AVG(TARGET) difficulty_rate FROM application_train GROUP BY 1 ORDER BY 3 DESC;'),
('Gender fairness audit only','SELECT CODE_GENDER, COUNT(*) applications, AVG(TARGET) difficulty_rate FROM application_train GROUP BY 1;'),
('Organization type','SELECT ORGANIZATION_TYPE, COUNT(*) applications, AVG(TARGET) difficulty_rate FROM application_train GROUP BY 1 HAVING COUNT(*)>=100 ORDER BY 3 DESC;'),
('Region rating','SELECT REGION_RATING_CLIENT, COUNT(*) applications, AVG(TARGET) difficulty_rate FROM application_train GROUP BY 1;'),
('Weekday','SELECT WEEKDAY_APPR_PROCESS_START, COUNT(*) applications, AVG(TARGET) difficulty_rate FROM application_train GROUP BY 1 ORDER BY 3 DESC;'),
('Application hour','SELECT HOUR_APPR_PROCESS_START, COUNT(*) applications, AVG(TARGET) difficulty_rate FROM application_train GROUP BY 1 ORDER BY 1;'),
('Median financial values','SELECT MEDIAN(AMT_INCOME_TOTAL), MEDIAN(AMT_CREDIT), MEDIAN(AMT_ANNUITY) FROM application_train;'),
('Missing values','SELECT COUNT(*) total_rows, SUM(CASE WHEN OCCUPATION_TYPE IS NULL THEN 1 ELSE 0 END) occupation_missing, SUM(CASE WHEN EXT_SOURCE_1 IS NULL THEN 1 ELSE 0 END) ext1_missing FROM application_train;'),
('Credit to income','SELECT AVG(AMT_CREDIT/NULLIF(AMT_INCOME_TOTAL,0)) avg_credit_income FROM application_train;'),
('Annuity to income','SELECT AVG(AMT_ANNUITY/NULLIF(AMT_INCOME_TOTAL,0)) avg_annuity_income FROM application_train;'),
('Age bands',"SELECT CASE WHEN -DAYS_BIRTH/365.25<25 THEN '18-24' WHEN -DAYS_BIRTH/365.25<35 THEN '25-34' WHEN -DAYS_BIRTH/365.25<45 THEN '35-44' WHEN -DAYS_BIRTH/365.25<55 THEN '45-54' WHEN -DAYS_BIRTH/365.25<65 THEN '55-64' ELSE '65+' END age_band, COUNT(*) applications, AVG(TARGET) difficulty_rate FROM application_train GROUP BY 1;"),
('Employment bands',"SELECT CASE WHEN DAYS_EMPLOYED>-365 THEN '<1 year' WHEN DAYS_EMPLOYED>-1825 THEN '1-5 years' WHEN DAYS_EMPLOYED>-3650 THEN '5-10 years' ELSE '10+ years' END employment_band, COUNT(*) applications, AVG(TARGET) difficulty_rate FROM application_train GROUP BY 1;"),
('Income quintiles','WITH x AS (SELECT *, NTILE(5) OVER(ORDER BY AMT_INCOME_TOTAL) q FROM application_train) SELECT q, COUNT(*) applications, AVG(TARGET) difficulty_rate FROM x GROUP BY q ORDER BY q;'),
('Credit by contract','SELECT NAME_CONTRACT_TYPE, AVG(AMT_CREDIT), MEDIAN(AMT_CREDIT) FROM application_train GROUP BY 1;'),
('Annuity by contract','SELECT NAME_CONTRACT_TYPE, AVG(AMT_ANNUITY) FROM application_train GROUP BY 1;'),
('Target counts by gender','SELECT CODE_GENDER, SUM(TARGET), COUNT(*) FROM application_train GROUP BY 1;'),
('External score averages','SELECT AVG(EXT_SOURCE_1), AVG(EXT_SOURCE_2), AVG(EXT_SOURCE_3) FROM application_train;'),
('Negative value checks','SELECT SUM(CASE WHEN AMT_INCOME_TOTAL<0 THEN 1 ELSE 0 END), SUM(CASE WHEN AMT_CREDIT<0 THEN 1 ELSE 0 END) FROM application_train;'),
('Duplicate IDs','SELECT SK_ID_CURR, COUNT(*) FROM application_train GROUP BY 1 HAVING COUNT(*)>1;'),
('Contract and weekday','SELECT NAME_CONTRACT_TYPE, WEEKDAY_APPR_PROCESS_START, COUNT(*), AVG(TARGET) FROM application_train GROUP BY 1,2 HAVING COUNT(*)>=100;'),
('Income type and education','SELECT NAME_INCOME_TYPE, NAME_EDUCATION_TYPE, COUNT(*), AVG(TARGET) FROM application_train GROUP BY 1,2 HAVING COUNT(*)>=100;'),
('Region by contract','SELECT NAME_CONTRACT_TYPE, REGION_RATING_CLIENT, COUNT(*), AVG(TARGET) FROM application_train GROUP BY 1,2;'),
('Weekday and hour','SELECT WEEKDAY_APPR_PROCESS_START, HOUR_APPR_PROCESS_START, COUNT(*), AVG(TARGET) FROM application_train GROUP BY 1,2;'),
('Segment size check','SELECT NAME_CONTRACT_TYPE, COUNT(*) FROM application_train GROUP BY 1 HAVING COUNT(*)>=500;')
]
sql='-- FinSight SQL portfolio. TARGET=1 means recorded historical payment difficulties.\n-- Table name assumed: application_train.\n'
for i,(title,q) in enumerate(queries,1):
    sql+='\n-- '+str(i)+'. '+title+'\n'+q+'\n'
(out/'sql'/'analysis_queries.sql').write_text(sql,encoding='utf-8')
(out/'powerbi'/'measures.dax').write_text(
"Applications = COUNTROWS('application_train')\nPayment Difficulty Cases = SUM('application_train'[TARGET])\nOther Cases = [Applications] - [Payment Difficulty Cases]\nPayment Difficulty Rate = DIVIDE([Payment Difficulty Cases], [Applications], 0)\nMedian Income = MEDIAN('application_train'[AMT_INCOME_TOTAL])\nMedian Credit = MEDIAN('application_train'[AMT_CREDIT])\nMedian Annuity = MEDIAN('application_train'[AMT_ANNUITY])\n",encoding='utf-8')
(out/'powerbi'/'dashboard_guide.md').write_text(
"Import data/application_train.csv into Power BI Desktop and name the table application_train.\nPage 1: KPI cards, TARGET outcome split, rate by contract type.\nPage 2: rate by income type, education, occupation and age band; show application count in tooltips.\nPage 3: income vs credit scatter and affordability ratios.\nPage 4: missingness profile from reports/missingness_profile.csv.\nValidate KPI cards against reports/executive_kpis.csv. TARGET=1 is historical recorded payment difficulty, not a causal or predictive label.\n",encoding='utf-8')
(rep/'executive_findings.md').write_text(
f"FinSight Analytics\nApplications: {n:,}\nRecorded payment difficulty cases: {target:,}\nOther cases: {n-target:,}\nHistorical rate: {rate:.2%}\nMedian income: {df.AMT_INCOME_TOTAL.median():,.0f} dataset currency units\nMedian credit: {df.AMT_CREDIT.median():,.0f}\nMedian annuity: {df.AMT_ANNUITY.median():,.0f}\n\nDescriptive historical analysis only. TARGET=1 is recorded payment difficulty, not necessarily legal default. No causal inference or predictive model. Show counts with rates; small groups can be unstable. Currency is not assumed INR. Demographic breakdowns are fairness-audit context only, not lending rules.\n",encoding='utf-8')
(rep/'interview_guide.md').write_text(
"Project summary: Analyzed historical credit applications using Python/pandas, profiled missingness, created segments, calculated KPIs, and prepared SQL and Power BI measures.\n\nTARGET=1 means recorded payment difficulties according to dataset definition. Report counts with rates because small groups can be unstable. Limitations: observational historical data, missing fields, possible selection effects, no causal inference, no predictive model or out-of-time validation. Be transparent about AI assistance and only claim work you can explain.\n",encoding='utf-8')
(out/'README.md').write_text(
f"FinSight generated deliverables. Source: {n:,} rows, {len(df.columns)} columns. Contains KPI and segment reports, missingness profile, charts, {len(queries)} SQL queries, DAX measures, dashboard guide and interview notes. Descriptive analysis only; no causal or predictive claims.\n",encoding='utf-8')
print(f'SUCCESS: {n:,} rows analyzed; {len(queries)} SQL queries and all deliverables created in {out}')
