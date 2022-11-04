{{config (materialized='table')}}

SELECT DISTINCT
event_id
, id AS seatgeek_performer_id
, CURRENT_TIMESTAMP AS cycle_date
FROM r_fact_seatgeek_performer_event_relationships