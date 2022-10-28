INSERT INTO r_dimension_spotify_tracks (
track_id
, track_name
, track_disc_number
, track_duration_ms
, track_explicit
, track_href
, track_is_local
, track_is_playable
, track_popularity
, track_preview_url
, track_number
, track_album_id
)

VALUES
(%s
, %s
, %s
, %s
, %s
, %s
, %s
, %s
, %s
, %s
, %s
, %s
)