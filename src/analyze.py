"""
FinSight data preparation and EDA.
Run from repository root:
  python src/analyze.py --input data/application_train.csv --output reports
Requires pandas, numpy, matplotlib.
"""
import argparse
from pathlib import Path
import pandas as pd
import numpy as np

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", default="data/application_train.csv")
    p.add_argument("--output", default="reports")
    args = p.parse_args()
    inp, out = Path(args.input), Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(inp)
    required = {"SK_ID_CURR", "TARGET", "AMT_INCOME_TOTAL", "AMT_CREDIT", "DAYS_BIRTH"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if df["SK_ID_CURR"].duplicated().any():
        raise ValueError("Duplicate application IDs detected; investigate before continuing.")

    # Explicit feature transformations; retain original source values in raw data.
    x = pd.DataFrame({
        "application_id": df["SK_ID_CURR"],
        "payment_difficulty": df["TARGET"].astype("int8"),
        "contract_type": df["NAME_CONTRACT_TYPE"],
        "gender": df["CODE_GENDER"],
        "income_type": df["NAME_INCOME_TYPE"],
        "education_type": df["NAME_EDUCATION_TYPE"],
        "family_status": df["NAME_FAMILY_STATUS"],
        "housing_type": df["NAME_HOUSING_TYPE"],
        "occupation_type": df["OCCUPATION_TYPE"],
        "organization_type": df["ORGANIZATION_TYPE"],
        "annual_income": df["AMT_INCOME_TOTAL"],
        "credit_amount": df["AMT_CREDIT"],
        "annuity_amount": df["AMT_ANNUITY"],
        "goods_price": df["AMT_GOODS_PRICE"],
        "age_years": -df["DAYS_BIRTH"] / 365.25,
        # Home Credit encodes 365243 as a special value for some employment records.
        "employment_years": np.where(df["DAYS_EMPLOYED"] < 0, -df["DAYS_EMPLOYED"] / 365.25, np.nan),
        "region_rating": df["REGION_RATING_CLIENT"],
        "external_score_1": df["EXT_SOURCE_1"],
        "external_score_2": df["EXT_SOURCE_2"],
        "external_score_3": df["EXT_SOURCE_3"],
        "bureau_queries_year": df["AMT_REQ_CREDIT_BUREAU_YEAR"],
        "social_defaults_30d": df["DEF_30_CNT_SOCIAL_CIRCLE"],
        "social_observations_30d": df["OBS_30_CNT_SOCIAL_CIRCLE"],
    })
    x["credit_to_income"] = x["credit_amount"] / x["annual_income"].replace(0, np.nan)
    x["annuity_to_income"] = x["annuity_amount"] / x["annual_income"].replace(0, np.nan)
    x["external_score_avg"] = x[["external_score_1","external_score_2","external_score_3"]].mean(axis=1)

    x.to_csv(out / "finsight_application_features.csv", index=False)
    df.isna().mean().mul(100).sort_values(ascending=False).rename("missing_pct").to_csv(out/"missingness_profile.csv")
    kpis = pd.DataFrame([{
        "applications": len(df),
        "payment_difficulty_cases": int(df["TARGET"].sum()),
        "other_cases": int((df["TARGET"] == 0).sum()),
        "payment_difficulty_rate": df["TARGET"].mean(),
        "median_income": df["AMT_INCOME_TOTAL"].median(),
        "median_credit": df["AMT_CREDIT"].median(),
        "median_annuity": df["AMT_ANNUITY"].median(),
    }])
    kpis.to_csv(out/"overall_kpis.csv", index=False)

    dimensions = ["contract_type","gender","income_type","education_type","family_status",
                  "housing_type","occupation_type","organization_type"]
    for col in dimensions:
        x.groupby(col, dropna=False).agg(
            applications=("application_id","count"),
            payment_difficulty_cases=("payment_difficulty","sum"),
            payment_difficulty_rate=("payment_difficulty","mean")
        ).reset_index().sort_values("applications", ascending=False).to_csv(
            out/f"risk_by_{col}.csv", index=False
        )
    print(f"Completed: {len(df):,} rows, {len(df.columns)} source columns")
    print(kpis.to_string(index=False))

if __name__ == "__main__":
    main()
