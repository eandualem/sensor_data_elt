{{ config(materialized='table') }}

with stations as (

    SELECT ID, FWY, DIR, District, County, City, State_PM, Abs_PM, Latitude, Longitude, Length, Type, Lanes, Name
    FROM dbtdb.I80Stations

)

select *
from stations