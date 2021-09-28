{{ config(materialized='table') }}

with final as (

    SELECT ID,flow_max,flow_median,flow_total,n_obs
    FROM dbtdb.station_summary

)

SELECT * FROM final
