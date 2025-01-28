from src.services.load_data import DataPreprocessor
from src.services.predict import SeafoodPricePredictor


model_paths = {
    "농어": "path/to/농어_model.pkl",
    "광어": "path/to/광어_model.pkl",
    "대게": "path/to/대게_model.pkl",
}

data_paths = {
    "농어": "path/to/농어_data.csv",
    "광어": "path/to/광어_data.csv",
    "대게": "path/to/대게_data.csv",
}

predictor = SeafoodPricePredictor(model_paths, data_paths)

# 특정 어종, 날짜, 시장에 대한 예측
result = predictor.predict("2025-01-25", market="Market 1", seafood="농어")
print("예측 결과:", result)

# 특정 시장과 날짜에 대한 전체 어종 예측
result = predictor.predict("2025-01-25", market="Market 1")
print("시장별 전체 어종 예측 결과:", result)

# 특정 날짜에 대한 전체 시장, 전체 어종 예측
result = predictor.predict("2025-01-25")
print("전체 예측 결과:", result)