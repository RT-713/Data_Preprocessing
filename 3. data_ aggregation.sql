-- ホテルIDをもとに抽出
-- nullでないreserve_idをカウント + 重複を削除したcustomer_idの数をカウント
select
hotel_id, count(reserve_id) as rev_cnt, count(distinct customer_id) as cus_cnt
from reserve_tb
group by hotel_id;

-- ホテルごとの宿泊人数別の合計予約金額を算出
select
hotel_id, people_num, sum(total_price) as price_sum
from reserve_tb
group by hotel_id, people_num;

-- テスト
select hotel_id,
       max(total_price) as c_max,
       min(total_price) as c_min,
       avg(total_price) as c_mean,
       percentile_cont(0.5) within group(order by total_price) as c_median,
       percentile_cont(0.2) within group(order by total_price) as c_20per
from reserve_tb
group by hotel_id 
;

select  * from reserve_tb rt ;