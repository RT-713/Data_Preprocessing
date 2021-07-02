# %% [markdown]
# ## 集約
# データ集約の意義は「データの価値を可能な限り損失せずにデータを圧縮し，データ単位（データ行が有する意味）を変換できる」ことにある．<br>
# A高校で実施された中間テスト
# - 中間テストの科目別平均点：テストの難易度を科目別に知ることができる<br>
# - 中間テストの生徒別平均点：個々の生徒の学力を把握できる<br>
# ### ＜集約を実現する方法＞
# 1. Groupbyで集約する単位を指定 → 集約関数（count, sum など）で処理
# 2. Window関数に対応する集約関数を使用する<br>
# ※一部のデータベースやプログラムではWindow関数の機能がないことも 
# %%
import numpy as np
import pandas as pd
# %%
reserve_tb = pd.read_csv('./data/reserve.csv', encoding='UTF-8')
reserve_tb.head()
# %%
reserve_tb.shape
# %% [markdown]
# ## データ数・種類数の算出
# %%
# groupbyとagg関数を使用することで集約と処理をひとまとめに
result = reserve_tb.groupby('hotel_id').agg({'reserve_id':'count', 'customer_id':'nunique'})
result
# %%
# reset_indexで行番号を再割り当て（inplace=Trueとしてもとのresultを更新）
result.reset_index(inplace=True)
result.columns = ['hotel_id', 'rsv_cnt', 'cus_cnt']
result
# %% [markdown]
# ## 合計値の算出
# 以下のコード（２パターン）はどちらもOK．
# - 集約処理がひとつの場合はagg関数を使用しない方が簡潔にコードを記載できる．<br>
# - 列名の変更もひとつだけならrename関数を使用しても複雑にはならない．
# %%
# 集約したデータからtotal_priceを取り出してsum関数で処理
result_sum =  reserve_tb.groupby(['hotel_id', 'people_num'])['total_price'].sum().reset_index()
result_sum
# %%
# 列名のリネーム
result_sum.rename(columns={'total_price':'price_sum'}, inplace=True)
result_sum
# %%
# パターン② 合計の算出にagg関数を使用 
result_sum2 = reserve_tb.groupby(['hotel_id', 'people_num']).agg({'total_price':'sum'}).reset_index()
result_sum2
# %%
result_sum2.rename(columns={'total_price':'price_sum'}, inplace=True)
result_sum2
# %% [markdown]
# ## 極値，代表値の算出
# %%
# 集約関数を使用してシンプルに実装する．
# total_priceの最大値・最小値・平均・中央値，20パーセンタイル点
result = reserve_tb.groupby('hotel_id').agg({'total_price':['max', 'min', 'mean', 'median', lambda x : np.percentile(x, q=20)]}).reset_index()
result
# %%
# 結果の列名を指定して表示する
result.columns = ['hotel_id', 'price_max', 'price_min', 'price_mean', 'price_median', 'price_20per']
result
# %%
# agg関数は列ごとに異なった処理も可能
result2 = reserve_tb.groupby('hotel_id').agg({'total_price':['max'], 'people_num':['mean']}).reset_index()
result2
# %%
# 集約関数で不偏分散と不偏標準偏差を算出
result = reserve_tb.groupby('hotel_id').agg({'total_price':['var', 'std']}).reset_index()
result.columns = ['hotel_id', 'price_var', 'price_std']
# NaNが発生した場合はその部分を0で埋める．
result.fillna(0, inplace=True)
result
# %% [markdown]
### 最頻値・順位の算出
# %%
# 最頻値を算出したい対象列を指定して，round関数で四捨五入，mode関数で最頻値を算出
reserve_tb['total_price'].round(-3).mode()
# %%
# 順位を算出するにはrank関数を使用する
# rank関数を適用するためにまずdatetime型に変換（rank関数は文字列型に対応していない）
reserve_tb['reserve_datetime'] = pd.to_datetime(reserve_tb['reserve_datetime'], format='%Y-%m-%d %H:%M:%S')'
# %%
reserve_tb['log_no'] = reserve_tb.groupby('customer_id')['reserve_datetime'].rank(ascending=True, method='first')
reserve_tb
# %%
