with I80_davis as (
    select * from {{ ref('I80_davis') }}
),

I80_stations as (
    select * from {{ ref('I80_stations') }}
)

select
    I80_davis.*,
    I80_stations.County,
    I80_stations.City,
    I80_stations.Latitude,
    I80_stations.Longitude
from I80_davis
left join I80_stations
on I80_davis.station_id = I80_stations.ID