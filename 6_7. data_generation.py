# %% [markdown]
# ## 生成
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