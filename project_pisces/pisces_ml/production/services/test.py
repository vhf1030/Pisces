# from src.production.services.load_data import DataPreprocessor
import sys
import os
current_dir = os.getcwd()
sys.path.append(current_dir)  # 루트 디렉터리 경로 추가  # .py

from pisces_ml.production.services.predict import SeafoodPricePredictor
import pandas as pd

# model_paths = {
#     "농어": "path/to/농어_model.joblib",
#     "광어": "path/to/광어_model.joblib",
#     "대게": "path/to/대게_model.joblib",
# }

# data_paths = {
#     "농어": "path/to/농어_data.csv",
#     "광어": "path/to/광어_data.csv",
#     "대게": "path/to/대게_data.csv",
# }

predictor = SeafoodPricePredictor()
predictor.model['광어']
predictor.data['광어']
date, fish, market = "2025-02-15", "광어", "노량진시장"
predictor.predict(date, fish, market)

fish_list = ["광어", "농어", "대게", "방어", "우럭", "참돔", "연어"]
for fish in fish_list:
    print(predictor.predict(date, fish, market))

for market in ["가락시장", "강서농수산물시장", "구리농수산물시장", "노량진시장", "마포농수산물시장", "부산민락어민활어직판장", "소래포구종합어시장", "수원농수산물시장", "안양평촌농수산물시장", "인천종합연안부두어시장"]:
    print(predictor.predict(date, fish, market))

