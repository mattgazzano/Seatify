{{config (materialized='table')}}

SELECT DISTINCT
event_id
, event_short_title AS event_title_short
, event_title AS event_title_full
, event_type
, event_datetime_tbd
, event_time_tbd
, event_datetime_utc
, event_datetime_local
, event_enddatetime_utc AS event_end_datetime_utc
, event_is_open
, event_visible_until_utc
, event_score
, event_popularity
, event_description
, event_status
, event_event_promotion AS event_promotion
, event_conditional
, CURRENT_TIMESTAMP AS cycle_date
FROM fact_seatgeek_performer_event_relationships