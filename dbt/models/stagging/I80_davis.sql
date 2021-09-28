with I80_davis as (
    select * from {{ ref('clean_I80_davis') }}
)

SELECT date_time, station_id, col3, col4, col5, col6, col7
FROM I80_davis