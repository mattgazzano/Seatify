CREATE TABLE IF NOT EXISTS r_fact_spotify_track_relationships (
artist_id VARCHAR
, artist_href VARCHAR
, artist_name VARCHAR
, artist_type VARCHAR
, artist_uri VARCHAR
, artist_external_urls_spotify VARCHAR
, track_name VARCHAR
, track_id VARCHAR
, track_disc_number INTEGER
, track_duration_ms INTEGER
, track_explicit BOOLEAN
, track_href VARCHAR
, track_is_local BOOLEAN
, track_is_playable VARCHAR
, track_popularity INTEGER
, track_preview_url VARCHAR
, track_number VARCHAR
, track_album_id VARCHAR
, cycle_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
)