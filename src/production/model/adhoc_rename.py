import joblib
import pandas as pd
import os

# 복사할 파일 목록  # 240129 진행
fish_list = ["광어", "농어", "대게", "방어", "우럭", "참돔", "연어"]
file_prefix = "lgbm_다중_"
file_suffix = ".joblib"
ori_dir = "tests/SY/LightGBM_선택됨/"
new_dir = "src/production/model/"
os.makedirs(new_dir, exist_ok=True)

for fish in fish_list:
    file_path = ori_dir + file_prefix + fish + file_suffix
    # 모델 로드
    model = joblib.load(file_path)
    print(model.get_params())
    print(model.estimators_[0].feature_name_)

    # 파일명만 추출하여 새 경로 생성
    new_path = new_dir + fish + "_model.joblib"

    # 새로운 이름으로 저장
    joblib.dump(model, new_path)
    print(f"{file_path} → {new_path}")


