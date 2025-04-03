import pandas as pd
from datetime import datetime, timedelta

def price_plot(fish, from_days):
    data_path = "pisces_ml/production/data/item_price_filled_pivot.csv"
    df = pd.read_csv(data_path)

    # 날짜 변환
    df["priceDate"] = pd.to_datetime(df["priceDate"])
    
    # 최근 `from_days`일만 필터링
    recent_date = df["priceDate"].max()
    df = df[df["priceDate"] >= (recent_date - pd.Timedelta(days=from_days))]

    # 어종별 가격 데이터
    fish_col = f"{fish}_avgPrice"

    # 시각화를 위한 데이터 변환
    df_filtered = df[["priceDate", "market", fish_col]].dropna()
    df_filtered = df_filtered.rename(columns={fish_col: "price"})

    # JSON 변환 (시장별 가격 변화를 날짜별로 그룹화)
    chart_data = {}
    for market, group in df_filtered.groupby("market"):
        chart_data[market] = {
            "dates": group["priceDate"].dt.strftime("%Y-%m-%d").tolist(),
            "prices": group["price"].tolist(),
        }

    return chart_data
