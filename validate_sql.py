from pathlib import Path
import csv, sqlite3, re, sys

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "application_train.csv"
SQL = ROOT / "deliverables" / "sql" / "analysis_queries.sql"
OUT = ROOT / "deliverables" / "sql" / "results"
OUT.mkdir(parents=True, exist_ok=True)

class Median:
    def __init__(self): self.values=[]
    def step(self, value):
        try:
            if value is not None and str(value).strip():
                self.values.append(float(value))
        except (TypeError, ValueError): pass
    def finalize(self):
        if not self.values: return None
        self.values.sort()
        n=len(self.values); mid=n//2
        return self.values[mid] if n%2 else (self.values[mid-1]+self.values[mid])/2

def main():
    if not DATA.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA}")
    sql_text=SQL.read_text(encoding="utf-8")
    titles=re.findall(r"(?m)^-- (\d+)\.\s(.*)$",sql_text)
    chunks=re.split(r"(?m)^-- \d+\.\s.*\n",sql_text)[1:]
    queries=[q.strip() for q in chunks if q.strip()]
    con=sqlite3.connect(":memory:")
    con.create_aggregate("MEDIAN",1,Median)
    with DATA.open("r",encoding="utf-8-sig",newline="") as f:
        reader=csv.reader(f); headers=next(reader)
        quote=lambda x: '"'+x.replace('"','""')+'"'
        con.execute("CREATE TABLE application_train ("+",".join(quote(h)+" TEXT" for h in headers)+")")
        marks=",".join("?" for _ in headers); batch=[]
        for row in reader:
            batch.append(row)
            if len(batch)>=4000:
                con.executemany(f"INSERT INTO application_train VALUES ({marks})",batch); batch=[]
        if batch: con.executemany(f"INSERT INTO application_train VALUES ({marks})",batch)
    con.commit()
    failures=[]
    for idx,(title,query) in enumerate(zip(titles,queries),1):
        number,name=title
        try:
            cur=con.execute(query)
            columns=[d[0] for d in cur.description] if cur.description else []
            rows=cur.fetchall()
            if columns:
                output=OUT/f"{int(number):02d}_{re.sub(r'[^a-z0-9]+','_',name.lower()).strip('_')}.csv"
                with output.open("w",encoding="utf-8",newline="") as f:
                    writer=csv.writer(f); writer.writerow(columns); writer.writerows(rows)
            print(f"PASS {number}: {name} ({len(rows)} rows)")
        except Exception as exc:
            failures.append((number,name,str(exc)))
            print(f"FAIL {number}: {name}: {exc}")
    con.close()
    report=ROOT/"deliverables"/"sql"/"SQL_VALIDATION_REPORT.md"
    report.write_text(
        "# SQL Validation Report\\n\\n"
        f"Executed {len(queries)} queries against the local dataset. "
        f"Passed: {len(queries)-len(failures)}; failed: {len(failures)}.\\n\\n"
        + ("\\n".join(f"- Query {n} ({name}): {err}" for n,name,err in failures) if failures else "All queries passed.")
        + "\\n\\nSQLite validation uses a custom MEDIAN aggregate. Adapt MEDIAN and any dialect-specific syntax for your target warehouse.\\n",
        encoding="utf-8")
    if failures: sys.exit(1)
    print(f"SUCCESS: {len(queries)} SQL queries passed.")

if __name__=="__main__": main()

