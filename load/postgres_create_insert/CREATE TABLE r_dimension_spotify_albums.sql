CREATE TABLE IF NOT EXISTS r_dimension_spotify_albums (
    album_id VARCHAR PRIMARY KEY
    , album_type VARCHAR
    , artists VARCHAR
    , available_markets VARCHAR
    , copyrights VARCHAR
    , genres VARCHAR
    , href VARCHAR
    , images VARCHAR
    , label VARCHAR
    , album_name VARCHAR
    , popularity INTEGER
    , release_date VARCHAR
    , release_date_precision VARCHAR
    , total_tracks INTEGER
    , record_type VARCHAR
    , uri VARCHAR
    , external_ids_upc VARCHAR
    , external_urls_spotify VARCHAR
    , tracks_href VARCHAR
    , tracks_items VARCHAR
    , tracks_limit INTEGER
    , tracks_next VARCHAR
    , tracks_offset INTEGER
    , tracks_previous VARCHAR
    , tracks_total INTEGER
    , cycle_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
)