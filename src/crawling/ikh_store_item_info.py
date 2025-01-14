import sys
import os
current_dir = os.getcwd()
sys.path.append(current_dir)  # 루트 디렉터리 경로 추가

import requests
import pandas as pd
import time
from data.data_source_item_mapping import IKH_MAPPING

file_path = "data/processed/ikh_store_meta_2025-01-13.csv"
df = pd.read_csv(file_path)
print(len(list(df["store_id"])))  # 153개 대상



# TODO: 
# 1. 마켓별 품목 확인
# 2. 품목별 공통되는 마켓 수 확인
# 3. 해당하는 마켓이 많은 품목에 대해 프로젝트 진행



