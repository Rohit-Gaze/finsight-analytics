# FinSight Analytics — Credit Risk & Business Intelligence Portfolio

A reproducible, descriptive analytics case study using the Home Credit Default Risk application-level dataset.

## Verified headline results
- 307,511 application records
- 24,825 records with TARGET=1
- 282,686 records with TARGET=0
- Historical TARGET=1 rate: 8.07%

`TARGET=1` means recorded payment difficulties under the dataset definition. It is not automatically equivalent to legal default, rejection, or a causal risk factor.

## Deliverables
- `src/analyze.py` — starter Python feature/report pipeline
- `build_finsight_complete.py` — generates charts, segment reports, KPIs, SQL/DAX support files
- `validate_sql.py` — runs the 30 SQL queries against the local CSV via SQLite and exports query results
- `deliverables/FinSight_Interactive_Dashboard.html` — interactive Plotly dashboard (open in a browser)
- `deliverables/FinSight_Analytics_Summary.xlsx` — Excel summary workbook
- `deliverables/reports/` — executive findings, KPI data, segment summaries, missingness, methodology, interview guide
- `deliverables/sql/analysis_queries.sql` — 30 business-oriented SQL queries
- `deliverables/sql/results/` — query output CSVs from validation
- `deliverables/powerbi/` — DAX measures and Power BI Desktop assembly guide

## Reproduce
Install dependencies listed in `requirements.txt`, put the source file at `data/application_train.csv`, then run:
```powershell
python build_finsight_complete.py
python validate_sql.py
```

## Dashboard
Open `deliverables/FinSight_Interactive_Dashboard.html` in Chrome or Edge for the interactive browser dashboard. A native Power BI `.pbix` must still be assembled and saved in Power BI Desktop using the included guide and DAX measures.

## Responsible interpretation
This is a historical observational dataset. Segment differences are associations, not proof of causation. The analysis does not train a predictive model, establish credit losses, or make lending decisions. Review missingness, sample sizes, fairness, privacy, and applicable regulations before operational use. Demographic breakdowns are audit/context only, not standalone adverse lending criteria. Financial values are dataset currency units and are not assumed INR.

## AI-use disclosure
AI tools assisted with scaffolding and documentation. Outputs were generated programmatically from the dataset. The project owner should personally review the analysis, reproduce key calculations, and be able to explain the work before presenting it in interviews.
