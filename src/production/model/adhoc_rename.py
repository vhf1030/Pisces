import pandas as pd
import joblib

model_path = '../../model/test/'

# 저장된 모델 및 피처 이름 로드
loaded_model = joblib.load(model_path + 'xgb_광어.joblib')
feature_names = joblib.load(model_path + 'feature_names.pkl')