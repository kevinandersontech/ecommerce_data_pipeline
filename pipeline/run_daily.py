
from datetime import datetime
from . import generate, validate, load
from .config import EXPORTS_DIR, WAREHOUSE_DB
from .utils import ensure_dirs
import duckdb, subprocess, pathlib

def main():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    # Step 1: generate synthetic CSVs
    generate.main()
    # Step 2: validate
    validate.main(today)
    # Step 3: load into DuckDB (creates warehouse/ecom.duckdb)
    load.load_day(today)
    # Step 4: run dbt (build models)
    subprocess.run(["dbt", "run", "--project-dir", "dbt", "--profiles-dir", "dbt"], check=True)
    # Step 5: export daily CSV from mart
    ensure_dirs(EXPORTS_DIR)
    con = duckdb.connect(WAREHOUSE_DB)
    df = con.execute("select * from mart_revenue_daily order by revenue_date desc").df()
    con.close()
    pathlib.Path(EXPORTS_DIR).mkdir(parents=True, exist_ok=True)
    df.to_csv(f"{EXPORTS_DIR}/revenue_daily.csv", index=False)
    print("Daily pipeline complete. Warehouse and exports are ready.")

if __name__ == "__main__":
    main()