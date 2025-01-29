import pandas as pd
import os

# 복사할 파일 목록  # 240129 진행
fish_list = ["광어", "농어", "대게", "방어", "우럭", "참돔"]
file_suffix = "_price_features_notnull.csv"
ori_dir = "data/features/final_oneHot/"
new_dir = "src/production/data/"
os.makedirs(new_dir, exist_ok=True)

for fish in fish_list:
    file_path = ori_dir + fish + file_suffix
    # 파일 로드
    df = pd.read_csv(file_path)

    # 파일명만 추출하여 새 경로 생성
    new_path = new_dir + fish + "_data.csv"

    # 새로운 이름으로 저장
    df.to_csv(new_path, index=False)
    print(f"{file_path} → {new_path}")


file_path = "data/features/final_oneHot/연어_price_features_notnull_노르웨이제외.csv"
new_path = "src/production/data/연어_data.csv"
df = pd.read_csv(file_path)
df.to_csv(new_path, index=False)
print(f"{file_path} → {new_path}")
