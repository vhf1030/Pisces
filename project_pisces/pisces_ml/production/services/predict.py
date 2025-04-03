import joblib  # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from datetime import datetime
# from .load_data import DataPreprocessor
from .metadata import FISH_INFO


class SeafoodPricePredictor:
    def __init__(self):
        """
        어종별 머신러닝 모델 경로와 데이터 경로를 받아 초기화합니다.
        """
        # self.data_preprocessor = DataPreprocessor()  # todo
        self.fish_list = ["광어", "농어", "대게", "방어", "우럭", "참돔", "연어"]
        self.market_list = ["가락시장", "강서농수산물시장", "구리농수산물시장", "노량진시장", "마포농수산물시장", "부산민락어민활어직판장", "소래포구종합어시장", "수원농수산물시장", "안양평촌농수산물시장", "인천종합연안부두어시장"]
        self.data_path = "pisces_ml/production/data/"
        self.model_path = "pisces_ml/production/model/"
        self.data = self.load_data()
        self.model = self.load_model()
        self.fish_info = FISH_INFO

    def load_data(self):
        """
        어종별 모델 추론에 활용할 데이터를 로드합니다.
        :return: 어종별 로드된 csv파일 딕셔너리
        """
        data_dict = {}
        for fish in self.fish_list:
            data = pd.read_csv(self.data_path + fish + '_data.csv')
            data['date'] = pd.to_datetime(data['date'])
            data_dict[fish] = data

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

    def predict(self, date, fish, market):
        """
        입력된 파라미터를 기반으로 수산물 가격을 예측합니다.
        """

        model = self.model[fish]
        data = self.data[fish].copy()
        # feature_names = [col for col in data.columns if col not in ['date', 'avgPrice']]
        feature_names = model.estimators_[0].feature_name_
        X = data[feature_names]

        input_data = X[
            (data['date'] == pd.Timestamp(date)) &
            (data['m_' + market] == 1)
        ]
        date_difference = 0
        if input_data.empty:
            last_date = data['date'].max()
            date_difference = (pd.Timestamp(date) - pd.Timestamp(last_date)).days
            # print(last_date, date_difference)
            input_data = X[
                (data['date'] == last_date) &
                (data['m_' + market] == 1)
            ]
            if date_difference >= 28:
                print(f"데이터가 부족하여 {date}를 예측할 수 없습니다.")
                return
            
        if input_data.empty:
            print(f"데이터가 부족하여 {market} {date} 를 예측할 수 없습니다.")
            return

        predicted_price = model.predict(input_data)[0][date_difference]
        result = {
            "date": date,
            "fish": fish,
            "info": self.fish_info[fish],
            "market": market,
            "predictions": predicted_price
        }
    
        return result

    def predict_fish(self, date, fish):
        '''
        특정 어종의 시장별 가격을 예측
        '''
        result = {}
        for market in self.market_list:
            result[market] = self.predict(date, fish, market)
        return result
    

    def predict_market(self, date, market):
        '''
        특정 시장의 어종별 가격을 예측
        '''
        result = {}
        for fish in self.fish_list:
            result[fish] = self.predict(date, fish, market)

        return result
        


