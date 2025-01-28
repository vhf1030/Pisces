import pickle
import numpy as np
from datetime import datetime
from src.services.load_data import DataPreprocessor

class SeafoodPricePredictor:
    def __init__(self, model_paths, data_paths):
        """
        어종별 머신러닝 모델 경로와 데이터 경로를 받아 초기화합니다.

        :param model_paths: 어종별 사전 학습된 머신러닝 모델 경로 딕셔너리 (예: {"농어": "path/to/농어_model.pkl"})
        :param data_paths: 어종별 데이터 파일 경로 딕셔너리 (예: {"농어": "path/to/농어_data.csv"})
        """
        self.model_paths = model_paths
        self.models = self.load_models()
        self.data_preprocessor = DataPreprocessor(data_paths)

    def load_models(self):
        """
        어종별 사전 학습된 머신러닝 모델을 로드합니다.

        :return: 어종별 로드된 머신러닝 모델 딕셔너리
        """
        models = {}
        for seafood, path in self.model_paths.items():
            try:
                with open(path, 'rb') as model_file:
                    models[seafood] = pickle.load(model_file)
            except FileNotFoundError:
                raise Exception(f"모델 파일이 경로 {path} 에서 발견되지 않았습니다.")
            except Exception as e:
                raise Exception(f"모델 로드 실패 ({seafood}): {e}")
        return models

    def preprocess_input(self, date, seafood):
        """
        데이터 전처리 클래스를 활용하여 입력 데이터를 전처리합니다.

        :param date: 예측 대상 날짜 (YYYY-MM-DD 형식)
        :param seafood: 어종 이름
        :return: 전처리된 데이터프레임
        """
        try:
            processed_data = self.data_preprocessor.preprocess(date, seafood)
            return processed_data
        except Exception as e:
            raise Exception(f"입력 데이터 전처리 실패 ({seafood}, {date}): {e}")

    def predict(self, date, market=None, seafood=None):
        """
        입력된 파라미터를 기반으로 수산물 가격을 예측합니다.

        :param date: 예측 대상 날짜 (YYYY-MM-DD 형식)
        :param market: (선택 사항) 시장 이름
        :param seafood: (선택 사항) 어종 이름
        :return: 예측 결과를 포함한 딕셔너리
        """
        if seafood and seafood not in self.models:
            raise Exception(f"{seafood}에 대한 모델이 존재하지 않습니다.")

        input_data = self.preprocess_input(date, seafood)

        try:
            if seafood:
                # 특정 어종에 대한 예측
                model = self.models[seafood]
                features = input_data.drop(columns=['date']).to_numpy()
                predictions = model.predict(features)
                return {"date": date, "market": market, "seafood": seafood, "price": predictions[0]}
            else:
                # 전체 어종에 대한 예측
                results = {}
                for seafood_name, model in self.models.items():
                    features = self.preprocess_input(date, seafood_name).drop(columns=['date']).to_numpy()
                    predictions = model.predict(features)
                    results[seafood_name] = predictions[0]
                return {"date": date, "market": market, "predictions": results}
        except Exception as e:
            raise Exception(f"예측 실패: {e}")

# 사용 예제
if __name__ == "__main__":
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
