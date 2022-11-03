
  
    

  create  table "seatify"."seatify"."dim_tracks__dbt_tmp"
  as (
    

SELECT DISTINCT
track_id
, track_album_id
, track_name
, track_disc_number
, track_number
, track_duration_ms
, (track_duration_ms / 60000) AS track_duration_minutes
, track_explicit
, track_is_local
, track_is_playable
, track_popularity
, CURRENT_TIMESTAMP AS cycle_date
FROM r_dimension_spotify_tracks
  );
  