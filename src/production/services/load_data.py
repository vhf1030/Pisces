import pandas as pd
from datetime import datetime

class DataPreprocessor:
    def __init__(self, data_paths):
        """
        어종별 데이터 경로를 받아 초기화합니다.

        :param data_paths: 어종별 데이터 파일 경로 딕셔너리 (예: {"농어": "path/to/농어_data.csv"})
        """
        self.data_paths = data_paths
        self.dataframes = self.load_data()

    def load_data(self):
        """
        어종별 데이터를 로드하여 pandas DataFrame으로 저장합니다.

        :return: 어종별 데이터프레임 딕셔너리
        """
        dataframes = {}
        for seafood, path in self.data_paths.items():
            try:
                dataframes[seafood] = pd.read_csv(path)
            except FileNotFoundError:
                raise Exception(f"데이터 파일이 경로 {path} 에서 발견되지 않았습니다.")
            except Exception as e:
                raise Exception(f"데이터 로드 실패 ({seafood}): {e}")
        return dataframes

    def preprocess(self, date, seafood):
        """
        입력된 날짜를 기준으로 해당 어종의 데이터를 전처리합니다.

        :param date: 기준 날짜 (YYYY-MM-DD 형식)
        :param seafood: 어종 이름
        :return: 전처리된 데이터프레임
        """
        if seafood not in self.dataframes:
            raise Exception(f"{seafood}에 대한 데이터가 존재하지 않습니다.")

        try:
            df = self.dataframes[seafood]

            # 날짜 필드가 있는지 확인
            if 'date' not in df.columns:
                raise Exception(f"데이터에 'date' 열이 없습니다 ({seafood}).")

            # 날짜 형식 변환
            df['date'] = pd.to_datetime(df['date'])
            target_date = pd.to_datetime(date)

            # 대상 날짜에 해당하는 데이터 필터링
            filtered_df = df[df['date'] == target_date]

            if filtered_df.empty:
                raise Exception(f"{seafood}에 대해 {date}에 해당하는 데이터가 없습니다.")

            # 필요한 전처리 로직 적용 (예: 결측값 처리, 범주형 인코딩 등)
            processed_df = filtered_df.fillna(0)  # 결측값을 0으로 대체 (예시)

            return processed_df
        except Exception as e:
            raise Exception(f"전처리 실패 ({seafood}, {date}): {e}")

# 사용 예제
if __name__ == "__main__":
    data_paths = {
        "농어": "path/to/농어_data.csv",
        "광어": "path/to/광어_data.csv",
        "대게": "path/to/대게_data.csv",
    }

    preprocessor = DataPreprocessor(data_paths)

    # 특정 날짜와 어종에 대한 데이터 전처리
    processed_data = preprocessor.preprocess("2025-01-25", seafood="농어")
    print(processed_data)
