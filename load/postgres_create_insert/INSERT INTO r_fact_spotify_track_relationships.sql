INSERT INTO r_fact_spotify_track_relationships (
artist_id
, artist_href
, artist_name
, artist_type
, artist_uri
, artist_external_urls_spotify
, track_name
, track_id
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
,%s
,%s
,%s
,%s
,%s
,%s
,%s
,%s
,%s
,%s
,%s
,%s
,%s
,%s
,%s
,%s
,%s
)