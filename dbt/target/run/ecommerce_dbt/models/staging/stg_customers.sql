
  
    
    

    create  table
      "ecom"."main"."stg_customers__dbt_tmp"
  
    as (
      select
  customer_id,
  country
from raw_customers
    );
  
  