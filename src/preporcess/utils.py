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


