CREATE TABLE IF NOT EXISTS r_dimension_spotify_artists (
artist_id VARCHAR PRIMARY KEY
, href VARCHAR
, images VARCHAR
, artist_name VARCHAR
, popularity INTEGER
, record_type VARCHAR
, uri VARCHAR
, external_urls_spotify VARCHAR
, followers_href VARCHAR
, followers_total INTEGER
, cycle_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
)