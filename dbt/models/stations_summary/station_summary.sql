{{ config(materialized='table') }}

with final as (

    SELECT *
    FROM dbtdb.station_summary

)

SELECT * FROM final
