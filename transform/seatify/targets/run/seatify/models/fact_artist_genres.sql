
  
    

  create  table "seatify"."seatify"."fact_artist_genres__dbt_tmp"
  as (
    

SELECT DISTINCT
artist_id
, genre
, CURRENT_TIMESTAMP AS cycle_date
FROM r_fact_spotify_artist_genres
  );
  