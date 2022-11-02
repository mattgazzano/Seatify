{{config (materialized='table')}}

{% set median_score_fields = ['event_score','event_popularity']%}

WITH fsp AS (
	SELECT
	*
	{% for field in median_score_fields %}
	, (SELECT PERCENTILE_CONT(.5) WITHIN GROUP (ORDER BY {{field}}) FROM r_fact_seatgeek_performer_event_relationships) AS median_{{field}}
	{% endfor %}
	FROM r_fact_seatgeek_performer_event_relationships
)

, fsp_pct AS (
	SELECT
	*
	{% for field in median_score_fields %}
	, CASE
		WHEN {{field}} != 0
			THEN ROUND((({{field}} - median_{{field}}) / ABS(median_{{field}}))::numeric,2)
		ELSE -1.00
	  END AS pct_above_median_{{field}}
	{% endfor %}
	FROM fsp
)

SELECT DISTINCT
event_id
, event_type
, event_short_title
, event_title
, event_created_at
, event_date_tbd
, event_time_tbd
, event_datetime_tbd
, event_datetime_local
, event_datetime_utc
, event_visible_until_utc
, event_enddatetime_utc
, DATE(event_announce_date) AS event_announce_date
, event_popularity
, pct_above_median_event_popularity
, event_score
, pct_above_median_event_score
, event_is_open
, CURRENT_TIMESTAMP AS cycle_date
FROM fsp_pct