CREATE TABLE IF NOT EXISTS r_dimension_spotify_tracks (
track_id VARCHAR PRIMARY KEY
, track_name VARCHAR
, track_disc_number INTEGER
, track_duration_ms INTEGER
, track_explicit BOOLEAN
, track_href VARCHAR
, track_is_local VARCHAR
, track_is_playable VARCHAR
, track_popularity INTEGER
, track_preview_url VARCHAR
, track_number INTEGER
, track_album_id VARCHAR
, cycle_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
)