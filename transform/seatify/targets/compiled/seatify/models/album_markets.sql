

SELECT DISTINCT
album_id
, alpha_2_code
, CURRENT_TIMESTAMP AS cycle_date
FROM r_fact_spotify_album_markets