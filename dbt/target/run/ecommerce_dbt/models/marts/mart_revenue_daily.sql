
  
    
    

    create  table
      "ecom"."main"."mart_revenue_daily__dbt_tmp"
  
    as (
      with f as ( select * from "ecom"."main"."fct_orders" )
select
  order_date as revenue_date,
  sum(case when status = 'paid' then order_amount else 0 end) as revenue_paid,
  sum(case when status = 'refunded' then order_amount else 0 end) as revenue_refunded,
  sum(case when status = 'failed' then order_amount else 0 end) as revenue_failed,
  sum(order_amount) as revenue_gross
from f
group by 1
order by 1
    );
  
  