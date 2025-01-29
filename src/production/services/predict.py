import joblib
import numpy as np
import pandas as pd
from datetime import datetime
# from src.production.services.load_data import DataPreprocessor


class SeafoodPricePredictor:
    def __init__(self):
        """
        어종별 머신러닝 모델 경로와 데이터 경로를 받아 초기화합니다.
        """
        # self.data_preprocessor = DataPreprocessor()  # todo
        self.fish_list = ["광어", "농어", "대게", "방어", "우럭", "참돔", "연어"]
        self.data_path = "src/production/data/"
        self.model_path = "src/production/model/"
        self.data = self.load_data()
        self.model = self.load_model()

    def load_data(self):
        """
        어종별 모델 추론에 활용할 데이터를 로드합니다.
        :return: 어종별 로드된 csv파일 딕셔너리
        """
        data_dict = {}
        for fish in self.fish_list:
            data_dict[fish] = pd.read_csv(self.data_path + fish + '_data.csv')

        return data_dict

    def load_model(self):
        """
        어종별 사전 학습된 머신러닝 모델을 로드합니다.
        :return: 어종별 로드된 머신러닝 모델 딕셔너리
        """
        model_dict = {}
        for fish in self.fish_list:
            model_dict[fish] = joblib.load(self.model_path + fish + '_model.joblib')

        return model_dict

    def predict(self, date, market=None, fish=None, num_days=1):
        # !!TODO!!
        """
        입력된 파라미터를 기반으로 수산물 가격을 예측합니다.
        """
        if fish and fish not in self.model:
            raise Exception(f"{fish}에 대한 모델이 존재하지 않습니다.")

        if fish:
            model = self.model[fish]
            data = self.data[fish].copy()
            # feature_names = [col for col in data.columns if col not in ['date', 'avgPrice']]
            feature_names = model.estimators_[0].feature_name_
        else:
            results = {}
            for fish_name in self.model.keys():
                results[fish_name] = self._predict_for_fish(date, fish_name, num_days)
            return {"date": date, "market": market, "predictions": results}

        return self._predict_for_fish(date, fish, num_days)

    def _predict_for_fish(self, start_date, fish, num_days):
        """
        특정 어종에 대한 시계열 예측을 수행합니다.
        """
        model = self.model[fish]
        data = self.data[fish].copy()
        feature_names = [col for col in data.columns if col not in ['date', 'avgPrice']]

        start_date = pd.Timestamp(start_date)
        rolling_data = data.copy()
        predictions = []

        for i in range(num_days):
            target_date = start_date + pd.Timedelta(days=i)
            previous_date = target_date - pd.Timedelta(days=1)

            input_data = rolling_data[rolling_data['date'] == previous_date]
            if input_data.empty:
                print(f"데이터가 부족하여 {target_date}를 예측할 수 없습니다.")
                break

            X = input_data[feature_names]
            predicted_price = model.predict(X)[0]

            predictions.append({'Date': target_date.strftime('%Y-%m-%d'), 'Predicted_Price': predicted_price})

            new_row = {'date': target_date, 'avgPrice': predicted_price}
            rolling_data = pd.concat([rolling_data, pd.DataFrame([new_row])], ignore_index=True)

        return predictions
