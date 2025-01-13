import sys
import os
current_dir = os.getcwd()
sys.path.append(current_dir)  # 루트 디렉터리 경로 추가

import requests
import pandas as pd
import time
from data.data_source_item_mapping import IKH_MAPPING


def get_price_data(item_id, market_code, period=1):
    url = f"https://pub-api.tpirates.com/v2/www/retail-price/item/{item_id}/period-price/{period}?&marketCodeList={market_code}"
    try:
        # Send GET request to the API
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        
        # Parse the JSON response
        data = response.json()
        return data
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

# get_price_data(IKH_MAPPING["item"]["광어"], IKH_MAPPING["market"]["노량진"], period=1)

# 수집 진행
def run_fetch():
    all_data = []
    period = 1000

    for item_name, item_id in IKH_MAPPING["item"].items():  # 각 품목과 시장에 대해 데이터 수집 및 통합
        for market_name, market_code in IKH_MAPPING["market"].items():
            print(f"Fetching data for item: {item_name} ({item_id}), market: {market_name} ({market_code})")
            data = get_price_data(item_id, market_code, period)
            if data:
                for entry in data:
                    entry["item"] = item_name
                    entry["market"] = market_name
                all_data.extend(data)
            time.sleep(1)

    # 데이터를 DataFrame으로 변환
    df = pd.DataFrame(all_data)
    # df.shape

    # 날짜 형식 변환
    if not df.empty:
        df["priceDate"] = pd.to_datetime(df["priceDate"])

    today = time.strftime("%Y-%m-%d")
    # today

    # 파일로 저장
    output_file = f"data/raw/ikh_data_{today}.csv"
    df.to_csv(output_file, index=False, encoding="utf-8")
