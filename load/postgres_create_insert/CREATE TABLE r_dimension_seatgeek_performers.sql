CREATE TABLE IF NOT EXISTS r_dimension_seatgeek_performers (
    seatgeek_performer_id INTEGER
    , spotify_artist_id VARCHAR
    , spotify_artists_url VARCHAR
    , provider VARCHAR
    , seatgeek_performers_type VARCHAR
    , seatgeek_performers_name VARCHAR
    , seatgeek_performers_image VARCHAR
    , seatgeek_performers_divisions VARCHAR
    , seatgeek_performers_has_upcoming_events BOOLEAN
    , seatgeek_performers_primary BOOLEAN
    , seatgeek_performers_image_attribution VARCHAR
    , seatgeek_performers_url VARCHAR
    , seatgeek_performers_score REAL
    , seatgeek_performers_slug VARCHAR
    , seatgeek_performers_home_venue_id VARCHAR
    , seatgeek_performers_short_name VARCHAR
    , seatgeek_performers_num_upcoming_events INTEGER
    , seatgeek_performers_colors VARCHAR
    , seatgeek_performers_image_license VARCHAR
    , seatgeek_performers_popularity INTEGER
    , seatgeek_performers_location VARCHAR
    , seatgeek_performers_image_rights_message VARCHAR
    , seatgeek_performers_images VARCHAR
    , seatgeek_performer_event_count VARCHAR
    , cycle_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
)