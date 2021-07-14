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
-- lag関数はn件前のデータを取得する関数lag(列名，n)
SELECT *,
	LAG(TOTAL_PRICE,2) OVER(PARTITION BY CUSTOMER_ID ORDER BY RESERVE_DATETIME) AS BEFORE_PRICE
FROM RESERVE_TB;

-- lead関数はn件後のデータを取得
SELECT *,
	LEAD(TOTAL_PRICE,3) OVER(PARTITION BY CUSTOMER_ID ORDER BY RESERVE_DATETIME) AS FORMER_PRICE
FROM RESERVE_TB;

-- 過去n件の合計値を算出
-- 検索CASE式を使用．（CASE <対象> WHEN <条件> THEN <処理> ELSE <条件外の処理> END）
-- 後ろn件としたい場合は「2 preceding -> 2 following」に変更すればOK
select *,
case when -- rows between <開始行> and <終了行> が文法（前2行から現在の行までが3行の場合，then以下の処理を実行）
count(total_price) over(partition by customer_id order by reserve_datetime rows between 2 preceding and current row) = 3
then
sum(total_price) over(partition by customer_id order by reserve_datetime rows between 2 preceding and current row)
else null end as price_sum-- 条件外の時はnullを入れる
from reserve_tb;

