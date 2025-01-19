
import pandas as pd

# 데이터 로드
file_path = "data/raw/ikh_item_price_2025-01-19.csv"
df = pd.read_csv(file_path)
df["priceDate"] = pd.to_datetime(df["priceDate"])


def fill_missing_dates(data, group_cols, date_col, target_cols):
    """
    날짜별 누락 데이터를 가장 최근 데이터로 채움.

    :param data: DataFrame
    :param group_cols: List[str], 그룹화 기준 컬럼
    :param date_col: str, 날짜 컬럼 이름
    :param target_cols: List[str], 채울 타겟 컬럼들
    :return: DataFrame, 누락된 날짜를 채운 데이터
    """

   # 모든 날짜를 포함한 DataFrame 생성
    full_date_range = (
        data.groupby(group_cols)
        .apply(lambda group: pd.DataFrame(
            {date_col: pd.date_range(start=group[date_col].min(), end=group[date_col].max())}
        ).assign(**{col: group[col].iloc[0] for col in group_cols}))  # 그룹 정보 추가
        .reset_index(drop=True)
    )

    # 원본 데이터와 병합
    full_data = pd.merge(full_date_range, data, on=group_cols + [date_col], how="left")

    # 결측값 채우기 (앞쪽 값으로 채움)
    full_data[target_cols] = (
        full_data.groupby(group_cols)[target_cols].apply(lambda group: group.fillna(method="ffill")).reset_index(drop=True)
    )

    return full_data


# Lag Feature 생성 함수
def create_lag_features(data, lags, group_cols, target_col):
    """
    Lag Features 생성.

    :param data: DataFrame
    :param lags: List[int], 시점 차이 (Lag) 리스트
    :param group_cols: List[str], 그룹화 기준 컬럼
    :param target_col: str, Lag Features를 생성할 타겟 컬럼
    :return: DataFrame, Lag Features 포함
    """
    data = data.sort_values(by=group_cols + ["priceDate"]).reset_index(drop=True)

    for lag in lags:
        lag_col_name = f"{target_col}_lag_{lag}"

        # 그룹화 및 Lag Feature 생성
        data[lag_col_name] = (
            data.groupby(group_cols, group_keys=False)
            .apply(lambda group: group[target_col].shift(lag))
            .reset_index(drop=True)
        )

    return data


# Lag Features 생성
lags = [1, 2, 3, 7]  # 하루 전, 이틀 전, 3일 전, 일주일 전
group_cols = ["item", "market"]  # 그룹화 기준
target_col = "avgPrice"  # 대상 컬럼


df_with_lags = create_lag_features(df, lags, group_cols, target_col)
df_with_lags.info()

output_file = f"data/processed/item_price_lag.csv"
df_with_lags.to_csv(output_file, index=False, encoding="utf-8")


# 누락 날짜 처리 (가장 최근의 가격으로)
date_col = "priceDate"
target_cols = ["minPrice", "avgPrice", "maxPrice"]

df_filled = fill_missing_dates(df, group_cols, date_col, target_cols)
df_with_lags_filled = create_lag_features(df_filled, lags, group_cols, target_col)
df_with_lags_filled.info()

output_file = f"data/processed/item_price_lag_filled.csv"
df_with_lags_filled.to_csv(output_file, index=False, encoding="utf-8")
