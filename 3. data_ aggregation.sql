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

-- ホテルごとに予約金額の極値（最大値・最小値）や代表値（平均値・四分位点）を算出
-- percentile_cout()は引数でパーセンタイル点を指定，within groupでorder byした列を対象にする．
select hotel_id,
       max(total_price) as c_max, -- 最大値
       min(total_price) as c_min, -- 最小値
       avg(total_price) as c_mean, -- 平均値
       percentile_cont(0.5) within group(order by total_price) as c_median,
       percentile_cont(0.2) within group(order by total_price) as c_20per
from reserve_tb
group by hotel_id 
;
/*
大規模データなどで処理が重い場合は，approximate percentile_disc関数を使ってもOK
・approximate percentile_disc関数はパーセンタイル値を近似的に出力する（相対誤差が0.5%程度だが高速）
・https://docs.aws.amazon.com/ja_jp/redshift/latest/dg/r_APPROXIMATE_PERCENTILE_DISC.html
<例> postgreSQLでは動かない．Amazon RedShift用かもしれない
select hotel_id,
       approximate percentile_disc(0.5) within group(order by total_price) as c_median,
from reserve_tb
group by hotel_id 
; 
 */

