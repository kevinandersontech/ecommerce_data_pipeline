
select
  order_id,
  sku,
  qty,
  unit_price,
  qty * unit_price as line_amount
from raw_order_items
