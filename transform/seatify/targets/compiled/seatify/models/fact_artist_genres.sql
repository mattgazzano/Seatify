

SELECT DISTINCT
artist_id
, genre
, CURRENT_TIMESTAMP AS cycle_date
FROM r_fact_spotify_artist_genres