
  
    

  create  table "seatify"."seatify"."fact_event_performers__dbt_tmp"
  as (
    

SELECT DISTINCT
event_id
, id AS seatgeek_performer_id
FROM r_fact_seatgeek_performer_event_relationships
  );
  