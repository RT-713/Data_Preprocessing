# %% [markdown]
# ## 6. 生成
# - オーバーサンプリング
# - アンダーサンプリング
# %%
# データの読み込み
import pandas as pd

production_tb = pd.read_csv('./data/production.csv')
production_tb.shape
# %%
production_tb[['fault_flg']].query('fault_flg == False').count()
# %%
production_tb[['fault_flg']].query('fault_flg == True').count()
# %% [markdown]
# ### SMOTEによるオーバーサンプリング
# オリジナルデータから新たなデータを作成するオーバーサンプリング
# - `radio`：不均衡データにおける少数データをどの程度（多数データの何割まで）増やすかを指定（auto=同じ数まで，0.5などの数値でも可能）
# - `k_neighbors`：kパラメータ
# %%
from imblearn.over_sampling import SMOTE

# インスタンス
sm = SMOTE(sampling_strategy='auto', k_neighbors=5, random_state=7)

# オーバーサンプリング処理
balance_data, balance_target = sm.fit_resample(production_tb[['length', 'thickness']], production_tb['fault_flg'])
# %%
# 同一の数までオーバーサンプリングできている
pd.DataFrame(balance_target).query('fault_flg == True').count()
# %% [markdown]
# ## 7. データ集計結果の展開
# #### 縦持ち・横持ちの変換
# %%
reserve_tb = pd.read_csv('./data/reserve.csv')
reserve_tb.head()
# %%
# pivot_table関数で実装
pd.pivot_table(reserve_tb, index='customer_id', columns='people_num', values='reserve_id', aggfunc=lambda x: len(x), fill_value=0)
# %% [markdown]
# ### 疎行列への変換
# %%
from scipy.sparse import csc_matrix

cnt_tb = reserve_tb.groupby(['customer_id', 'people_num'])['reserve_id'].size().reset_index()
cnt_tb.columns = ['customer_id', 'people_num', 'rsv_cnt']
cnt_tb
# %%
# customer_idをカテゴリー型へ変換
customer_id = pd.Categorical((cnt_tb['customer_id']))
people_num = pd.Categorical((cnt_tb['people_num']))

csc_matrix((cnt_tb['rsv_cnt'], (customer_id.codes, people_num.codes)), shape=(len(customer_id.categories), len (people_num.categories)))
# %%
