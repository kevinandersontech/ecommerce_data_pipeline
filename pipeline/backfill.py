from datetime import datetime, timedelta
import argparse, subprocess
from . import generate, validate, load

def main(days: int):
    end = datetime.utcnow().date()
    start = end - timedelta(days=days-1)
    for i in range(days):
        d = start + timedelta(days=i); ds = d.strftime("%Y-%m-%d")
        print(f"Backfilling {ds}")
        generate.main(start=ds, end=ds); validate.main(ds); load.load_day(ds)
    subprocess.run(["dbt", "deps"], cwd="dbt", check=True)
    subprocess.run(["dbt", "run"], cwd="dbt", check=True)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=30)
    args = ap.parse_args(); main(args.days)
