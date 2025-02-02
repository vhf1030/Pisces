import pandas as pd
import glob
import sys
import os

current_dir = os.getcwd()
sys.path.append(current_dir)  # 루트 디렉터리 경로 추가  # .py
sys.path.append(os.path.dirname(current_dir))  # 상위 디렉터리 경로 추가  # .ipynb
# from src.crawling.nst_item_search import *
from src.preporcess.utils import create_pivot_table, create_aggregate_table, find_missing_dates, fill_missing_dates_and_forward_fill

data_dir = "data/"

def prep_price(
        input_path="data/raw/ikh_item_price_2025-01-30.csv",
        out_path="data/prep_0131/item_price_filled_pivot.csv"
    ):
    ### 가격 데이터 전처리
    # input: "raw/ikh_item_price_2025-01-30.csv"
    # output: "prep_0131/item_price_filled_pivot.csv"

    # 가격 데이터 널값 제거
    df = pd.read_csv(input_path)
    df["priceDate"] = pd.to_datetime(df["priceDate"])

    group_cols = ["item", "market"]  # 그룹화 기준
    target_col = "avgPrice"  # 대상 컬럼
    date_col = "priceDate"

    # 모든 날짜를 포함한 DataFrame 생성
    full_date_range = (
        df.groupby(group_cols)
        .apply(lambda group: pd.DataFrame(
            {date_col: pd.date_range(start=group[date_col].min(), end=group[date_col].max())}
        ).assign(**{col: group[col].iloc[0] for col in group_cols}))  # 그룹 정보 추가
        .reset_index(drop=True)
    )

    # 원본 데이터와 병합
    full_data = pd.merge(full_date_range, df, on=group_cols + [date_col], how="left")

    # 결측값 채우기 (앞쪽 값으로 채움)
    full_data[target_col] = (
        full_data.groupby(group_cols)[target_col].apply(lambda group: group.fillna(method="ffill")).reset_index(drop=True)
    )

    # 불필요한 컬럼 제거
    full_data.drop(["minPrice", "maxPrice"], axis=1, inplace=True)

    # 노량진 2층 제거
    full_data = full_data[full_data['market'] != '노량진 2층']
    full_data['market'] = full_data['market'].replace('노량진 1층', '노량진시장')

    # 피벗 테이블 생성
    item_price_filled_pivot = create_pivot_table(
        df=full_data,
        index_cols=['priceDate', 'market'],  # 기준 컬럼
        columns_col='item',                  # 분류 기준
        values_col='avgPrice'                # 값 컬럼
    )

    item_price_filled_pivot.to_csv(out_path, index=False)


def prep_trend(
    input_path_pattern="data/raw/nst_*_2025-01-30.csv",
    out_path="data/prep_0131/search_trend_pivot.csv"
):
    file_list = glob.glob(input_path_pattern)
    df_list = [pd.read_csv(file_path) for file_path in file_list]
    df = pd.concat(df_list, ignore_index=True).drop("idx", axis=1)

    search_trend_pivot = create_pivot_table(
        df=df,
        index_cols=['date', 'age'],  # 기준 컬럼
        columns_col='name',                  # 분류 기준
        values_col='score'                # 값 컬럼
    )
    search_trend_pivot.to_csv(out_path, index=False)


def prep_forecast(
    input_path_pattern="data/raw/forecast_1525/forecast_*.csv",
    out_path="data/prep_0131/forecast_agg.csv"
):
    file_list = glob.glob(input_path_pattern)
    df_list = [pd.read_csv(file_path, encoding='euc-kr') for file_path in file_list]
    df = pd.concat(df_list, ignore_index=True)
    column_mapping = {
        '풍속(m/s)': '풍속',
        '풍향(deg)': '풍향',
        'GUST풍속(m/s)': 'GUST풍속',
        '현지기압(hPa)': '현지기압',
        '습도(%)': '습도',
        '기온(°C)': '기온',
        '수온(°C)': '수온',
        '최대파고(m)': '최대파고',
        '유의파고(m)': '유의파고',
        '평균파고(m)': '평균파고',
        '파주기(sec)': '파주기',
        '파향(deg)': '파향'
    }
    df_tmp = df.rename(columns=column_mapping)
    df_tmp['일시'] = pd.to_datetime(df_tmp['일시']).dt.date
    agg_funcs = {
        '풍속': 'mean',                # 평균 풍속
        'GUST풍속': 'mean',           # 평균 돌풍 풍속
        '현지기압': 'mean',            # 평균 현지 기압
        '습도': 'mean',                  # 평균 습도
        '기온': 'mean',               # 평균 기온
        '수온': 'mean',         # 평균 수온
        '최대파고': 'max',            # 최대 파고
        '유의파고': 'mean',   # 평균 유의 파고
        '평균파고': 'mean',       # 평균 파고
        '파주기': 'mean',               # 평균 파주기
    }
    forecast_agg = create_aggregate_table(df_tmp, index_cols=['지점', '일시'], agg_funcs=agg_funcs)
    forecast_agg.to_csv(out_path, index=False)




# # 시장 데이터 원핫 인코딩
# # 시장별 더미변수 생성 (0, 1로 인코딩)
# market_dummies = pd.get_dummies(df_pivot['market'], prefix='m').astype(int)

#     # priceDate 칼럼명을 date로 변경
# df_pivot = df_pivot.rename(columns={'priceDate': 'date'})

# # 원본 데이터와 더미변수 결합
# df_m_onehot = pd.concat([
#     df_pivot[['date']],  # 'priceDate' → 'date'로 변경됨
#     market_dummies,
#     df_pivot[[c for c in df_pivot.columns if "avgPrice" in c]]
# ], axis=1)

# print(df_m_onehot[df_m_onehot['m_가락시장'] == 1])
# print(df_m_onehot.columns)
# # 가격데이터 어종별로 나누고 lag1 생성해서 저장하기
# fish_list = ['광어', '농어', '대게', '방어', '연어', '우럭', '참돔']
# for fish in fish_list:
#     continue



# df = pd.read_csv('item_price_oneHot.csv')

# for fish in df['item'].unique():
#     fish_df = df[df['item'] == fish]
#     output_file = f'{fish}_price_oneHot.csv'
#     # fish_df = fish_df.drop('item', axis=1)
#     fish_df.to_csv(output_file, index=False)
#     print(f'{fish} 데이터 생성 완료: {len(fish_df)}개 행')
    