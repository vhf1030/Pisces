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
print(len(list(df["store_id"])))  # 153개 대상


def get_store_menu(store_id, store=None):
    url = f"https://pub-api.tpirates.com/v3/www/stores/{store_id}/products"
    response = requests.get(url)
    data = response.json()
    
    result = []
    for k in data['keywords']:
        for prod in k['products']:
            name = prod['name']
            if 'prices' not in prod:
                continue
            
            for pric in prod['prices']:
                tmp = {
                    "store_id": store_id,
                    "store": store,
                    'name': name,
                    'menu_id': pric['id'],
                    'menu': pric['name'],
                    'price': pric['price'],
                    'discount': pric['discountPrice'],
                    'unit_value': pric['unitValue'],
                    'unit': pric['unit']
                }
                result.append(tmp)
                
    return result
# test = get_store_menu("0000000200")


def run_fetch():
    all_data = []
    # for query in IKH_MAPPING["market"]:
    for row in df.itertuples():
        market, store_id, store = row.market, row.store_id, row.store
        data = get_store_menu(store_id, store)
        all_data.extend(data)
        print(f"market: {market}, store_id: {store_id}, store: {store}\t, {len(data)}", flush=True)
        time.sleep(1)

    result = pd.DataFrame(all_data)

    today = time.strftime("%Y-%m-%d")

    # 파일로 저장
    output_file = f"data/raw/ikh_store_menu_{today}.csv"
    result.to_csv(output_file, index=False, encoding="utf-8")

# run_fetch()


