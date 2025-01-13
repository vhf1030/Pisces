import matplotlib.pyplot as plt
import koreanize_matplotlib
import platform
import seaborn as sns


# OS에 따라 한글 폰트 설정
if platform.system() == "Windows":
    plt.rcParams["font.family"] = "Malgun Gothic"  # Windows: 맑은 고딕
elif platform.system() == "Darwin":
    plt.rcParams["font.family"] = "AppleGothic"   # macOS: 애플 고딕
else:
    plt.rcParams["font.family"] = "NanumGothic"   # Linux: 나눔 고딕 (사전 설치 필요)

plt.rcParams["axes.unicode_minus"] = False




import sys
import os
current_dir = os.getcwd()
sys.path.append(current_dir)  # 루트 디렉터리 경로 추가

import requests
import pandas as pd
import time
from crawling.ikh_item_price import get_price_data
from data.data_source_item_mapping import IKH_MAPPING


get_price_data(IKH_MAPPING["item"]["광어"], IKH_MAPPING["market"]["노량진"], period=1)

IKH_MAPPING["market"]
IKH_MAPPING["item"]["연어"]
# https://pub-api.tpirates.com/v2/www/retail-price/item/3920/period-price/1?

get_price_data(IKH_MAPPING["item"]["광어"], IKH_MAPPING["market"]["노량진"], period=1)

# TODO: 시장별로 데이터가 많은 품목 확인 필요
#  - 연어 1kg의 경우 노량진, 가락, 영등포, 자갈치의 데이터가 없음 - 만약 한다면, 100g로 진행하는 방안
#  -  
