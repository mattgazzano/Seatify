
  
    

  create  table "seatify"."seatify"."dim_country_codes__dbt_tmp"
  as (
    

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
FROM r_dimension_country_codes
  );
  