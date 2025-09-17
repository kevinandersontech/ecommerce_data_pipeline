with o as ( select * from "ecom"."main"."stg_orders" ),
     i as ( select * from "ecom"."main"."stg_order_items" ),
agg as (
  select
    o.order_id,
    o.customer_id,
    cast(o.order_ts as date) as order_date,
    sum(i.line_amount) as order_amount,
    any_value(o.status) as status
  from o join i using(order_id)
  group by 1,2,3
)
select * from agg