import pandas as pd


def create_pivot_table(df, index_cols, columns_col, values_col):
    """
    피벗 테이블 생성 함수.
    
    Args:
        df (pd.DataFrame): 입력 데이터프레임.
        index_cols (list): 기준 컬럼 리스트 (피벗 테이블의 인덱스 컬럼).
        columns_col (str): 분류 기준 컬럼명 (피벗 테이블의 컬럼).
        values_col (str): 값 컬럼명 (피벗 테이블에 채울 값).

    Returns:
        pd.DataFrame: 생성된 피벗 테이블.
    """
    # 피벗 테이블 생성
    pivot_df = df.pivot_table(
        index=index_cols,
        columns=columns_col,
        values=values_col
    )
    
    # 다중 컬럼 이름 정리 (예: '광어' -> '광어_avgPrice')
    pivot_df.columns = [f"{col}_{values_col}" for col in pivot_df.columns]
    
    # 인덱스 초기화
    pivot_df.reset_index(inplace=True)
    
    return pivot_df


def create_aggregate_table(df, index_cols, agg_funcs):
    """
    데이터 집계 테이블 생성 함수.

    Args:
        df (pd.DataFrame): 입력 데이터프레임.
        index_cols (list): 기준 컬럼 리스트 (그룹화할 컬럼).
        agg_funcs (dict): 각 컬럼에 대해 적용할 집계 함수의 딕셔너리.

    Returns:
        pd.DataFrame: 생성된 집계 테이블.
    """
    # 데이터 그룹화 및 집계
    agg_df = df.groupby(index_cols).agg(agg_funcs)

    # 인덱스 초기화
    agg_df.reset_index(inplace=True)

    return agg_df


def find_missing_dates(df, date_col):
    """
    데이터프레임에서 누락된 날짜를 확인하는 함수.

    Args:
        df (pd.DataFrame): 입력 데이터프레임.
        date_col (str): 날짜를 나타내는 컬럼명.

    Returns:
        pd.DatetimeIndex: 누락된 날짜 목록.
    """
    # 날짜 컬럼이 datetime 형식인지 확인
    if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
        df[date_col] = pd.to_datetime(df[date_col])

    # 날짜 범위 생성
    full_date_range = pd.date_range(start=df[date_col].min(), end=df[date_col].max())

    # 존재하는 날짜와 전체 범위 비교
    existing_dates = pd.to_datetime(df[date_col]).sort_values().unique()
    missing_dates = full_date_range.difference(existing_dates)

    return missing_dates


def fill_missing_dates_and_forward_fill(df, date_col):
    """
    누락된 날짜를 추가하고, 결측치를 이전 날짜의 가장 최근 값으로 채우는 함수.

    Args:
        df (pd.DataFrame): 입력 데이터프레임.
        date_col (str): 날짜 컬럼명.

    Returns:
        pd.DataFrame: 누락된 날짜가 추가되고 결측치가 채워진 데이터프레임.
    """
    df_tmp = df.copy()
    
    # 날짜 컬럼을 datetime 형식으로 변환
    df_tmp[date_col] = pd.to_datetime(df_tmp[date_col])
    
    # 전체 날짜 범위 생성
    full_date_range = pd.date_range(start=df_tmp[date_col].min(), end=df_tmp[date_col].max())
    
    # 날짜를 인덱스로 설정
    df_tmp.set_index(date_col, inplace=True)
    
    # 누락된 날짜를 추가
    df_tmp = df_tmp.reindex(full_date_range)
    
    # 인덱스를 다시 날짜로 설정
    df_tmp.index.name = date_col
    
    # 결측치를 이전 값으로 채우기
    df_tmp.ffill(inplace=True)
    
    # 인덱스를 다시 컬럼으로 변환
    df_tmp.reset_index(inplace=True)
    
    return df_tmp

