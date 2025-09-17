select
  order_id,
  customer_id,
  cast(strptime(order_ts_iso, '%Y-%m-%dT%H:%M:%S') as timestamp) as order_ts,
  status
from raw_orders