-- 数値型の変換処理
SELECT 
-- 整数型
cast((40000 / 3) as integer) AS integer,
cast((40000 / 3) as bigint) AS bigint,

-- 浮動小数点型
cast((40000 / 3) as numeric) AS numeric,
cast((40000 / 3) as double precision) AS double_precision,

-- textもいける
cast((40000 / 3) as text) AS text

FROM reserve_tb
LIMIT 1;

-- 対数化処理
-- total_priceを1000で除して1を加算した結果を対数化（底は10）
select *, log(total_price / 1000 + 1) from reserve_tb limit 20;

-- カテゴリに分ける処理
-- floor関数で小数点以下を切り捨てる（例：41 → (41/10)=4.1 → 4.0*10 → 40=40代）
-- より高度なカテゴリ分けをしたいならCASE式を使用するなどが必要
select *, floor(age / 10)*10 as age_rank from customer_tb limit 20;