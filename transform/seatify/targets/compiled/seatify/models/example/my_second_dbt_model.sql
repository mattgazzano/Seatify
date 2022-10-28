-- Use the `ref` function to select from other models

select *
from "seatify_lake"."seatify_lake"."my_first_dbt_model"
where id = 1