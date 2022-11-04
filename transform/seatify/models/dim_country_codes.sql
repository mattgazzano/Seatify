{{config (materialized='table')}}

SELECT DISTINCT
country
, alpha_2_code
, alpha_3_code
, numeric_code
, latitude
, longitude
, continent
, CAST(population AS float) AS population
, percentage_of_world
, CURRENT_TIMESTAMP AS cycle_date
FROM r_dimension_country_codes