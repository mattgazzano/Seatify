INSERT INTO r_dimension_spotify_artists (
    artist_id
    , href
    , images
    , artist_name
    , popularity 
    , record_type
    , uri
    , external_urls_spotify
    , followers_href
    , followers_total) 

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
    )