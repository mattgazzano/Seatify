INSERT INTO r_dimension_spotify_albums (
    album_id
    , album_type
    , artists
    , available_markets
    , copyrights
    , genres
    , href
    , images
    , label
    , album_name
    , popularity
    , release_date
    , release_date_precision
    , total_tracks
    , record_type
    , uri
    , external_ids_upc
    , external_urls_spotify
    , tracks_href
    , tracks_items
    , tracks_limit
    , tracks_next
    , tracks_offset
    , tracks_previous
    , tracks_total
)

VALUES( 
    %s
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
    , %s
    , %s
)