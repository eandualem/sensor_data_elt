with final as (

    SELECT ID, FWY, DIR, District, County, City, Name, Latitude, Longitude
    FROM dbtdb.I80Stations

)

SELECT * FROM final