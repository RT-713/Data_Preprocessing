-- マスターテーブルの結合
-- 必要な情報のみを扱うように注意を払うこと
select
r.reserve_id, r.hotel_id, r.customer_id, r.reserve_datetime, r.checkin_date , 
r.checkin_time, r.checkout_date, r.people_num, r.total_price,
h.base_price, h.big_area_name, h.small_area_name, h.hotel_latitude, h.hotel_longitude, h.is_business
from
reserve_tb as r
join
hotel as h
on 
r.hotel_id = h.hotel_id
and h.is_business is true  -- on句に加えて条件を追記
and r.people_num = 1; --同上

-- 条件に応じたテーブル結合の切り替え
with small_area_mst as(
select 
small_area_name,
case when count(hotel_id)-1 >= 20
then small_area_name else big_area_name end as join_area_id
from hotel
group by big_area_name, small_area_name
)

,recommend_hotel_mst as (
select 
big_area_name as join_area_id,
hotel_id as rec_hotel_id
from hotel 
union
select
small_area_name as join_area_id,
hotel_id as rec_hotel_id
from hotel
)

select
hotels.hotel_id, r_hotel_mst.rec_hotel_id
from hotel as hotels
inner join small_area_mst s_area_mst 
on hotels.small_area_name = s_area_mst.small_area_name
inner join recommend_hotel_mst r_hotel_mst
on s_area_mst.join_area_id = r_hotel_mst.join_area_id
and hotels.hotel_id != r_hotel_mst.rec_hotel_id;

-- n件前のデータ取得



