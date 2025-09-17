import duckdb, pandas as pd
from pathlib import Path
from .config import RAW_DIR, WAREHOUSE_DB
from .utils import ensure_dirs

DDL_ORDERS = """create table if not exists raw_orders(
 order_id text primary key, customer_id text, order_ts_iso text, status text );"""
DDL_ITEMS = """create table if not exists raw_order_items(
 order_id text, sku text, qty int, unit_price double );"""
DDL_CUSTOMERS = """create table if not exists raw_customers(
 customer_id text primary key, country text );"""

def load_day(ds: str) -> None:
    ensure_dirs("warehouse")
    con = duckdb.connect(WAREHOUSE_DB)
    for ddl in (DDL_ORDERS, DDL_ITEMS, DDL_CUSTOMERS): con.execute(ddl)
    o = pd.read_csv(Path(RAW_DIR)/f"orders_{ds}.csv")
    i = pd.read_csv(Path(RAW_DIR)/f"order_items_{ds}.csv")
    c = pd.read_csv(Path(RAW_DIR)/f"customers_{ds}.csv")
    con.register("tmp_o", o); con.execute("delete from raw_orders using tmp_o where raw_orders.order_id = tmp_o.order_id"); con.execute("insert into raw_orders select * from tmp_o"); con.unregister("tmp_o")
    con.register("tmp_i", i); con.execute("insert into raw_order_items select * from tmp_i"); con.unregister("tmp_i")
    con.register("tmp_c", c); con.execute("delete from raw_customers using tmp_c where raw_customers.customer_id = tmp_c.customer_id"); con.execute("insert into raw_customers select * from tmp_c"); con.unregister("tmp_c")
    con.close()

if __name__ == "__main__":
    import sys; load_day(sys.argv[1])
