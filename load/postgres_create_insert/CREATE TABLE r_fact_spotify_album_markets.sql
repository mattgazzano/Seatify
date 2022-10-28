CREATE TABLE IF NOT EXISTS r_fact_spotify_album_markets (
album_id VARCHAR
, alpha_2_code VARCHAR
, cycle_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
)