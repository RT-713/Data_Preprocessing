# %% [markdown]
# ## 第2章 抽出
# %%
import numpy as np
import pandas as pd
# %%
reserve_tb = pd.read_csv('./data/reserve.csv', encoding='UTF-8')
reserve_tb.head()
# %%
reserve_tb.shape
# %% [markdown]
# ## 列を抽出するときのコード記載
# - 列は列名で指定した方が可読性よし！
# %%
# 列名抽出①
reserve_tb[['reserve_id', 'hotel_id', 'customer_id',
            'reserve_datetime','checkin_date', 'checkin_time', 'checkout_date']].head()
# %%
# 列名抽出②
reserve_tb.loc[:, ['reserve_id', 'hotel_id', 'customer_id',
            'reserve_datetime','checkin_date', 'checkin_time', 'checkout_date']].head()
# %% [markdown]
# ## 例外
# - 余分な列を落とすことで表示したい列を持ってくる．<br>
# - axisで列を指定し，inplaceで呼び出し元のdfに変更を適用．<br>
# 可読性は低くなるが，大元のdfのデータを落とすので処理が軽くなる．
# %%
# 列名抽出③ 
# reserve_tb.drop(['people_num', 'total_price'], axis=1, inplace=True)
# reserve_tb（あとに影響が出るため，コメントアウト）
# %% [markdown]
# ## 条件によるデータ行の抽出
# %%
# queryを使用すればOK
# 文字列ならシングルクォート内でさらにダブルクォートを使用して指定
reserve_tb.query('"2016-10-13" <= checkout_date <= "2016-10-14"')
# %%
# 通常の数字などであれば以下のような実装でよい
reserve_tb.query('500000 < total_price')
# %% [markdown]
# ## 行単位でランダムサンプリングを行う
# %%
# pandasのsample関数（行単位のサンプリング）を使って実装
reserve_tb.sample(frac=0.5) # fraction：割合・比，ほんの一部，かけら
# %% [markdown]
# ## IDに基づくサンプリング（公正なサンプリング）
# %%
# 顧客単位のランダムサンプリングで50%の行を抽出
# 顧客IDをサンプリング
target = pd.Series(reserve_tb['customer_id'].unique()).sample(frac=0.5)
target
# %%
# isin関数：customer_idとサンプリングした顧客IDの一致を確認し，行を抽出
reserve_tb[reserve_tb['customer_id'].isin(target)]