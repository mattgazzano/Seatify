INSERT INTO r_dimension_seatgeek_performers (
    seatgeek_performer_id
    , spotify_artist_id
    , spotify_artists_url
    , provider
    , seatgeek_performers_type
    , seatgeek_performers_name
    , seatgeek_performers_image
    , seatgeek_performers_divisions
    , seatgeek_performers_has_upcoming_events
    , seatgeek_performers_primary
    , seatgeek_performers_image_attribution
    , seatgeek_performers_url
    , seatgeek_performers_score
    , seatgeek_performers_slug
    , seatgeek_performers_home_venue_id
    , seatgeek_performers_short_name
    , seatgeek_performers_num_upcoming_events
    , seatgeek_performers_colors
    , seatgeek_performers_image_license
    , seatgeek_performers_popularity
    , seatgeek_performers_location
    , seatgeek_performers_image_rights_message
    , seatgeek_performers_images
    , seatgeek_performer_event_count
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
, %s)