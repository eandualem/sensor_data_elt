with final as (

    SELECT timestamp, totalflow, weekday, hour, minute, second
    FROM dbtdb.richards

)

SELECT * FROM final