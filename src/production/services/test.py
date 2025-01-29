# from src.production.services.load_data import DataPreprocessor
import sys
import os
current_dir = os.getcwd()
sys.path.append(current_dir)  # 루트 디렉터리 경로 추가  # .py

from src.production.services.predict import SeafoodPricePredictor


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

predictor.predict("2024-12-25")



# # 특정 어종, 날짜, 시장에 대한 예측
# result = predictor.predict("2025-01-25", market="Market 1", seafood="농어")
# print("예측 결과:", result)

# # 특정 시장과 날짜에 대한 전체 어종 예측
# result = predictor.predict("2025-01-25", market="Market 1")
# print("시장별 전체 어종 예측 결과:", result)

# # 특정 날짜에 대한 전체 시장, 전체 어종 예측
# result = predictor.predict("2025-01-25")
# print("전체 예측 결과:", result)