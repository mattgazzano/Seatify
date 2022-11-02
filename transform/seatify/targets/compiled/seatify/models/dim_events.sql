



WITH fsp AS (
	SELECT
	*
	
	, (SELECT PERCENTILE_CONT(.5) WITHIN GROUP (ORDER BY event_score) FROM r_fact_seatgeek_performer_event_relationships) AS median_event_score
	
	, (SELECT PERCENTILE_CONT(.5) WITHIN GROUP (ORDER BY event_popularity) FROM r_fact_seatgeek_performer_event_relationships) AS median_event_popularity
	
	FROM r_fact_seatgeek_performer_event_relationships
)

, fsp_pct AS (
	SELECT
	*
	
	, CASE
		WHEN event_score != 0
			THEN ROUND(((event_score - median_event_score) / ABS(median_event_score))::numeric,2)
		ELSE -1.00
	  END AS pct_above_median_event_score
	
	, CASE
		WHEN event_popularity != 0
			THEN ROUND(((event_popularity - median_event_popularity) / ABS(median_event_popularity))::numeric,2)
		ELSE -1.00
	  END AS pct_above_median_event_popularity
	
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