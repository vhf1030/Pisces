import sys
import os
current_dir = os.getcwd()
sys.path.append(current_dir)  # 루트 디렉터리 경로 추가

import requests
import pandas as pd
import time
from data.data_source_item_mapping import IKH_MAPPING

file_path = "data/processed/ikh_store_meta_2025-01-13.csv"
df = pd.read_csv(file_path, dtype={"store_id": str})
# print(len(list(df["store_id"])))  # 153개 대상


def get_store_item(store_id, store=None):
    # print("search_keywords:", [k for k in IKH_MAPPING])
    url = f"https://pub-api.tpirates.com/v2/www/retail-price/store/{store_id}/latest-price?page=0&size=2000"
    response = requests.get(url)
    data = response.json()
    
    result = []
    for c in data['content']:
        tmp = {
            "store_id": store_id,
            "store": store,
        } | c
        tmp.pop("thumbnails")
        
        result.append(tmp)
    return result
# get_store_item("0000001155")

def run_fetch():
    all_data = []
    # for query in IKH_MAPPING["market"]:
    for row in df.itertuples():
        market, store_id, store = row.market, row.store_id, row.store
        data = get_store_item(store_id, store)
        all_data.extend(data)
        print(f"market: {market}, store_id: {store_id}, store: {store}\t, {len(data)}", flush=True)
        time.sleep(1)

    result = pd.DataFrame(all_data)

    today = time.strftime("%Y-%m-%d")

    # 파일로 저장
    output_file = f"data/raw/ikh_store_item_{today}.csv"
    result.to_csv(output_file, index=False, encoding="utf-8")

# run_fetch()
