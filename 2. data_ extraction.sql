-- 列の抽出
select reserve_id, hotel_id, checkin_date from reserve_tb;

-- 条件によるデータ行の抽出
select * from reserve_tb where checkin_date between '2016-07-01' and '2016-07-31';

-- インデックスを間接的に利用したデータ行の抽出（checkoutデータを抽出したい）
-- ×：そのままcheckout_dateを読み込ませると全部のデータを確認するのでデータへのアクセス量が増加するので
-- ○：インデックスがcheckin_dateに付与されていることを利用する
select * from reserve_tb where checkin_date between '2016/10/10' and '2016/10/13' 
and checkout_date between '2016/10/13' and '2016_10/14';

-- ランダムサンプリング（予約テーブルからランダムに50%分を取り出す）
-- 乱数を作成できるrandom()を使用（randomは0.00-1.00の間で乱数を生成）
-- データ数が十分に多い時は偏りを気にせずに以下のコードでOK（余分な処理がないので高速）
select * from  reserve_tb where random() <= 0.5;

-- ID単位のサンプリングを行う＝トリッキーな方法が必要
with reserve_tb_random as (select *, first_value(random()) over (partition by customer_id) as random_num from reserve_tb) 
select * from reserve_tb_random where random_num <= 0.5;