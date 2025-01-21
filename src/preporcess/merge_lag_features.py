
import pandas as pd

# 데이터 로드
file_path = "data/raw/ikh_item_price_2025-01-19.csv"
df = pd.read_csv(file_path)
df["priceDate"] = pd.to_datetime(df["priceDate"])
df





