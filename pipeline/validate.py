import pandas as pd
from pathlib import Path
from .config import RAW_DIR

def _must(path: Path): 
    if not path.exists(): raise FileNotFoundError(f"Missing file: {path}")

def validate_day(ds: str) -> None:
    o = Path(RAW_DIR)/f"orders_{ds}.csv"
    i = Path(RAW_DIR)/f"order_items_{ds}.csv"
    c = Path(RAW_DIR)/f"customers_{ds}.csv"
    for p in (o,i,c): _must(p)
    df_o = pd.read_csv(o); df_i = pd.read_csv(i); df_c = pd.read_csv(c)
    assert df_o["order_id"].is_unique, "order_id must be unique"
    assert df_c["customer_id"].is_unique, "customer_id must be unique"
    assert df_o["status"].isin(["paid","refunded","failed"]).all(), "invalid order status"
    assert df_i["order_id"].isin(df_o["order_id"]).all(), "items ref missing orders"
    assert df_o["customer_id"].isin(df_c["customer_id"]).all(), "orders ref missing customers"
    assert (df_i["qty"]>0).all(), "qty must be positive"
    assert (df_i["unit_price"]>=0).all(), "price must be non negative"

def main(ds: str): validate_day(ds)
if __name__ == "__main__":
    import sys; main(sys.argv[1])
