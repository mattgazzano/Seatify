CREATE TABLE IF NOT EXISTS r_dimension_country_codes (
    country VARCHAR
    , alpha_2_code VARCHAR
    , alpha_3_code VARCHAR
    , numeric_code INTEGER
    , latitude REAL
    , longitude REAL
    , country_rank VARCHAR
    , continent VARCHAR
    , population VARCHAR
    , percentage_of_world VARCHAR
    , wikipedia_date_retrieved VARCHAR
    , wikipedia_source VARCHAR
    , notes TEXT
    , cycle_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
)