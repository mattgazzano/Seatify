INSERT INTO r_dimension_country_codes (
    country
    , alpha_2_code
    , alpha_3_code
    , numeric_code
    , latitude
    , longitude
    , country_rank
    , continent
    , population
    , percentage_of_world
    , wikipedia_date_retrieved
    , wikipedia_source
    , notes
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
, %s)