import random, csv
from datetime import datetime, timedelta
from pathlib import Path
from .config import RAW_DIR, SEED_ROWS_PER_DAY
from .utils import ensure_dirs

random.seed(42)
PRODUCTS = [
    {"sku":"A100","name":"Widget Alpha","price":19.0},
    {"sku":"B200","name":"Gadget Beta","price":49.0},
    {"sku":"C300","name":"Toolset Gamma","price":99.0},
]

def daterange(s, e):
    d = s
    while d <= e:
        yield d
        d += timedelta(days=1)

def generate_day(day: datetime, outdir: Path) -> None:
    num_orders = max(1, int(random.gauss(SEED_ROWS_PER_DAY, SEED_ROWS_PER_DAY*0.2)))
    orders = outdir / f"orders_{day:%Y-%m-%d}.csv"
    items = outdir / f"order_items_{day:%Y-%m-%d}.csv"
    customers = outdir / f"customers_{day:%Y-%m-%d}.csv"
    cust_ids = [f"CUST{1000+i}" for i in range(max(25, num_orders//4))]
    with open(orders, "w", newline="") as fo, open(items, "w", newline="") as fi, open(customers, "w", newline="") as fc:
        o = csv.DictWriter(fo, fieldnames=["order_id","customer_id","order_ts_iso","status"]); o.writeheader()
        i = csv.DictWriter(fi, fieldnames=["order_id","sku","qty","unit_price"]); i.writeheader()
        c = csv.DictWriter(fc, fieldnames=["customer_id","country"]); c.writeheader()
        for cid in cust_ids:
            c.writerow({"customer_id":cid,"country":random.choice(["AU","US","UK","DE"])})
        for k in range(num_orders):
            oid = f"ORD{day:%Y%m%d}{k:05d}"; cid = random.choice(cust_ids)
            status = random.choices(["paid","refunded","failed"], weights=[0.9,0.05,0.05])[0]
            o.writerow({"order_id":oid,"customer_id":cid,"order_ts_iso":day.strftime("%Y-%m-%dT%H:%M:%S"),"status":status})
            for _ in range(random.randint(1,3)):
                prod = random.choice(PRODUCTS); qty = random.randint(1,3)
                i.writerow({"order_id":oid,"sku":prod["sku"],"qty":qty,"unit_price":prod["price"]})

def main(start: str|None=None, end: str|None=None):
    ensure_dirs(RAW_DIR); outdir = Path(RAW_DIR)
    if not start or not end:
        d = datetime.utcnow().date()
        return generate_day(datetime(d.year,d.month,d.day), outdir)
    s = datetime.fromisoformat(start); e = datetime.fromisoformat(end)
    for day in daterange(s,e):
        generate_day(datetime(day.year,day.month,day.day), outdir)

if __name__ == "__main__":
    main()
