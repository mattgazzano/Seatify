
    
    

select
    event_id as unique_field,
    count(*) as n_records

from "seatify_lake"."seatify_lake"."dimension_seatgeek_events"
where event_id is not null
group by event_id
having count(*) > 1


