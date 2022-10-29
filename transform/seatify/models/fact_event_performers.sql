{{config (materialized='table')}}

SELECT DISTINCT
event_id
, id AS performer_id
FROM r_fact_seatgeek_performer_event_relationships;