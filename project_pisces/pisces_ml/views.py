from django.shortcuts import render  # type: ignore
from django.http import JsonResponse  # type: ignore
import os
import json
from datetime import datetime, date, timedelta
# Create your views here.

from pisces_ml.production.services.predict import SeafoodPricePredictor
from pisces_ml.production.services.visualization import price_plot

predictor = SeafoodPricePredictor()


def market_overview(request):
    # !TODO!
    # 예시 데이터 로드 (JSON 파일 또는 DB에서 가져오기)
    data_path = os.path.join('static', 'data', 'market_prices.json')
    with open(data_path, 'r') as file:
        market_data = json.load(file)
    
    context = {'market_data': market_data}
    return render(request, 'pisces_ml/market_overview.html', context)


def price_visualization(request):
    days = int(request.GET.get("days", 365))  # 사용자가 선택한 날짜 범위 (기본값: 365일)

    # 가격 데이터 로드 (각 어종별 그래프를 위한 데이터 준비)
    fish_types = ["광어", "우럭", "참돔", "연어", "대게", "방어", "농어"]  # 전체 어종 목록
    chart_data = {fish: price_plot(fish, days) for fish in fish_types}  # 어종별 시각화 데이터 수집

    # JSON 변환 (한글 깨짐 방지)
    chart_data_json = json.dumps(chart_data, ensure_ascii=False)

    return render(request, "pisces_ml/price_chart.html", {
        "chart_data": chart_data_json,
        "selected_days": days,
        "fish_types": fish_types,
    })


def predict_fish(request):
    result = None  # 기본값 설정

    if request.method == 'POST':
        fish = request.POST.get('fish')
        date = request.POST.get('date')

        if fish and date:
            result = predictor.predict_fish(date, fish)
            item_info = predictor.fish_info[fish]
            context = {
                'fish': fish,
                'date': date,
                'result': result,
                'item_info': item_info
            }
            print("예측 결과:", context)  # 터미널에서 확인
            
        return render(request, 'pisces_ml/fish_template.html', context)

    return render(request, 'pisces_ml/fish_template.html', {'fish': None, 'date': None})


def predict_market(request):
    result = None  # 기본값 설정

    if request.method == 'POST':
        market = request.POST.get('market')
        date = request.POST.get('date')

        if market and date:
            result = predictor.predict_market(date, market)
            context = {
                'market': market,
                'date': date,
                'result': result
            }
            print("예측 결과:", context)  # 터미널에서 확인

        return render(request, 'pisces_ml/market_template.html', context)

    return render(request, 'pisces_ml/market_template.html', {'market': None, 'date': None})


# def index(request):
#     return render(request, 'pisces_ml/index.html')

# # 임시 모델 예측 함수 (머신러닝 모델 로드 시 대체)
# def mock_predict(market, item, date):
#     # 예시: 시장 이름, 품목, 날짜를 기반으로 간단한 예측
#     return f"{hash(market) % 100 * 10 + hash(item) % 1000 * 100 + hash(date.split('-')[2]) % 100 * 10}원"

def predict_page(request):
    """입력 폼 및 결과 페이지"""
    return render(request, 'pisces_ml/predict.html')

def predict(request):  # to be deprecated
    """예측 요청 처리"""
    if request.method == 'POST':
        market = request.POST.get('market')
        item = request.POST.get('item')
        date = request.POST.get('date')
        try:
            if not market or not item or not date:
                raise ValueError("All fields are required.")

            prediction = predictor.predict(date, item, market)
            # fish_info = predictor.fish_info
            # return JsonResponse({'prediction': prediction})
            print(prediction)
            
            context = {
                'prediction': round(prediction['predictions']),
                # 'item_info': fish_info[item],
                'item_info': prediction['info']
            }
            return JsonResponse(context)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
