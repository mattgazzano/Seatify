
  
    

  create  table "seatify"."seatify"."dim_albums__dbt_tmp"
  as (
    

WITH dsa AS (
	SELECT
	*
	, CASE release_date_precision
		WHEN 'year'
	  		THEN DATE(CONCAT(CAST(release_date AS VARCHAR),'-01-01'))
	  	WHEN 'month'
	  		THEN DATE(CONCAT(CAST(release_date AS VARCHAR),'-01'))
	 	WHEN 'day'
	 		THEN DATE(release_date)
	  END AS release_date_cleaned
	FROM r_dimension_spotify_albums
)

SELECT DISTINCT
album_id
, album_type
, album_name
, label
, popularity
, release_date
, release_date_precision
, release_date_cleaned
, (CURRENT_DATE - release_date_cleaned) AS days_since_release_date
, total_tracks
, CURRENT_TIMESTAMP AS cycle_date
FROM dsa
  );
  