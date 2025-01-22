
import pandas as pd
from pycaret.regression import setup, compare_models, get_config, pull, predict_model
import matplotlib.pyplot as plt
import koreanize_matplotlib

def run_automl_feature_importance(data, target, time_series_split=False):
    # PyCaret 설정
    if time_series_split is True:
        fold_strategy = "timeseries"
        data_split_shuffle = False
        fold_shuffle = False
    else:
        fold_strategy = "kfold"
        data_split_shuffle = True
        fold_shuffle = True
    setup(
        data=data,
        target=target,
        session_id=1030,  # 재현성을 위한 난수 시드
        normalize=True,  # 데이터 스케일링
        fold_strategy=fold_strategy,
        data_split_shuffle=data_split_shuffle,
        fold_shuffle=fold_shuffle,
        verbose=False
    )

    # 여러 모델 비교 및 최적 모델 선정
    best_model = compare_models(
        include=["rf", "lightgbm", "xgboost", "catboost"],
        verbose=False)
    
    # 최적 모델 이름과 평가지표 출력
    print("Best Model:", type(best_model).__name__)
    print("Model Performance Metrics:")
    metrics = pull()  # PyCaret에서 비교된 모델들의 평가지표를 가져옴
    print(metrics.loc[metrics.index[0]])  # 최적 모델의 성능만 출력
    
    importances = best_model.feature_importances_
    processed_features = get_config("X_train_transformed").columns
    feature_importance_df = pd.DataFrame({
        "Feature": processed_features,
        "Importance": importances
    }).sort_values(by="Importance", ascending=False)
    
    plt.figure(figsize=(10, 6))
    feature_importance_df.plot(kind="bar", x="Feature", y="Importance", legend=False, color="skyblue")
    plt.title("Feature Importance")
    plt.ylabel("Importance")
    plt.xlabel("Features")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()
    return best_model

