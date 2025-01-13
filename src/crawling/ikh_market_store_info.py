import sys
import os
current_dir = os.getcwd()
sys.path.append(current_dir)  # 루트 디렉터리 경로 추가

import requests
import pandas as pd
import time
from data.data_source_item_mapping import IKH_MAPPING


def get_store_info(s_query):
    # print("search_keywords:", [k for k in IKH_MAPPING])
    url = f"https://pub-api.tpirates.com/v2/www/market/filter/list?keyword={s_query}&sort=default"
    response = requests.get(url)
    data = response.json()
    
    result = []
    for c in data['content']:
        tmp = {
            "s_query": s_query,
            "market": c["market"],
            "store": c["label"],
            "store_id": c["id"],
            "comments": c["summary"]["comments"],
            "like": c["summary"]["like"],
            "rating": c["summary"]["rating"],
        }
        result.append(tmp)
    return result

# test = get_market_store_info("가락")
# pprint.pp(test)

def run_fetch():
    all_data = []
    # for query in IKH_MAPPING["market"]:
    market_list = [
        "노량진", "가락", "강서", "마포", "영등포", "마장", "구리", "수원", "평촌",
        "경기", "소래포구", "연안부두", "인천", "강원", "경상", "부산", "울산"]
    for query in market_list:
        data = get_store_info(query)
        all_data.extend(data)
        print(query, "\t", len(data), flush=True)
        time.sleep(1)

    df = pd.DataFrame(all_data)

    today = time.strftime("%Y-%m-%d")

    # 파일로 저장
    output_file = f"data/raw/ikh_store_meta_{today}.csv"
    df.to_csv(output_file, index=False, encoding="utf-8")
    
run_fetch()
