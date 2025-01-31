import pandas as pd
import glob
import sys
import os

current_dir = os.getcwd()
sys.path.append(current_dir)  # 루트 디렉터리 경로 추가  # .py
sys.path.append(os.path.dirname(current_dir))  # 상위 디렉터리 경로 추가  # .ipynb
# from src.crawling.nst_item_search import *
from src.preporcess.utils import create_pivot_table, create_aggregate_table, find_missing_dates, fill_missing_dates_and_forward_fill

data_dir = "data/"


# 가격 데이터 널값 제거
file_path = data_dir + "raw/ikh_item_price_2025-01-30.csv"
df = pd.read_csv(file_path)
df["priceDate"] = pd.to_datetime(df["priceDate"])
df

df_pivot = create_pivot_table(
    df=df,
    index_cols=['priceDate', 'market'],  # 기준 컬럼
    columns_col='item',                  # 분류 기준
    values_col='avgPrice'                # 값 컬럼
)
print(len(df_pivot["market"].unique()))
print(find_missing_dates(df_pivot, "priceDate"))
df_pivot

df_filled = fill_missing_dates_and_forward_fill(df_pivot, date_col="priceDate")
df_filled









file_path = "processed_0131/item_price_lag_filled.csv"
df = pd.read_csv(data_dir + file_path)
df


