
  
    

  create  table "seatify"."seatify"."dimension_artists__dbt_tmp"
  as (
    

WITH dsp AS (
	SELECT
	dsp.*
	,  RIGHT(spotify_artist_id,22) AS spotify_artist_id_cleaned
	, (SELECT PERCENTILE_CONT(.5) WITHIN GROUP (ORDER BY seatgeek_performers_score) FROM r_dimension_seatgeek_performers) AS median_seatgeek_performers_score
	FROM r_dimension_seatgeek_performers dsp
)

SELECT DISTINCT
dsa.artist_id AS spotify_artist_id
, dsa.popularity AS spotify_popularity
, dsa.followers_total AS total_spotify_followers
, CASE
	WHEN dsp.seatgeek_performer_id IS NOT NULL
		THEN TRUE
	ELSE FALSE
  END AS has_performer_record
, dsp.seatgeek_performer_id
, dsa.artist_name
, dsp.seatgeek_performers_short_name
, dsp.seatgeek_performers_image
, dsp.seatgeek_performers_has_upcoming_events
, dsp.seatgeek_performers_primary
, dsp.seatgeek_performers_url
, dsp.seatgeek_performers_score
, dsp.median_seatgeek_performers_score
, CASE
	WHEN dsp.seatgeek_performers_score != 0
		THEN ((dsp.seatgeek_performers_score - dsp.median_seatgeek_performers_score) / ABS(dsp.median_seatgeek_performers_score))
	WHEN dsp.seatgeek_performer_id IS NOT NULL
		THEN -1
  END AS seatgeek_performer_pct_above_median_score
 , CURRENT_TIMESTAMP AS cycle_date
FROM r_dimension_spotify_artists dsa
LEFT JOIN dsp
	ON dsa.artist_id = dsp.spotify_artist_id_cleaned
  );
  