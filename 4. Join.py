# %% [markdown]
# ## 結合
# データがまとまっている場合は少なく，多くの場合は分散して存在している．<br>
# 各データを集約して処理できるように結合手法について記載する．
# %%
import pandas as pd

reserve_tb = pd.read_csv('./data/reserve.csv')
hotel_tb = pd.read_csv('./data/hotel.csv')
# %% [markdown]
# ### merge関数の適用前にはデータを必要最低限に抑える．
# よくない例<br>
# `pd.merge(reserve_tb, hotel_tb, on='hotel_id', how='inner').query('people_num == 1 & is_business')`<br>
# 先にすべてを結合させてからクエリで絞り込んでいるためNG．先に絞り込んでから結合させる．
# %%
# merge関数の引数に指定するテーブルは事前に条件で絞ることができる
rsv_hotel = pd.merge(reserve_tb.query('people_num == 1'), hotel_tb.query('is_business'), on='hotel_id', how='inner')
rsv_hotel
# %% [markdown]
# ### 条件に応じた結合テーブルの切り替え
# 長すぎるので省略
# %% [markdown]
# ## `shift関数`：n件前・後のデータを取得して列を作成
# %%
# customerごとにreserve_datetimeで並び替え
result = reserve_tb.groupby('customer_id').apply(lambda group: group.sort_values(by='reserve_datetime', axis=0, inplace=False))
result
# %%
# shift関数を使用してbefore_price列に2つ前のtotal_priceを入れる
result['before_price'] = pd.Series(result['total_price'].groupby('customer_id').shift(periods=2))
result
# %%
# SQLでは前のデータを取得するには異なる関数が必要だったが，Pythonではperiodsを負にすればOK
result['former_price'] = pd.Series(result['total_price'].groupby('customer_id').shift(periods=-3))
result
# %% [markdown]
# ## 過去n日間の合計値
# %%
