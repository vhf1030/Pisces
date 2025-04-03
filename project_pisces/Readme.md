# Pisces ML: 수산물 가격 예측 서비스

Pisces ML은 10개의 마켓과 7종의 수산물을 대상으로 한 머신러닝 기반 수산물 가격 예측 웹 애플리케이션입니다. 이 프로젝트는 사용자가 원하는 날짜, 수산물, 시장 정보를 기반으로 예측 가격을 제공하고, 현재까지의 시장 시가를 시각화하는 기능을 제공합니다.
- 어종 리스트: 농어, 광어, 대게, 연어, 우럭, 참돔, 방어
- 시장 리스트: 가락시장, 강서농수산물시장, 구리농수산물시장, 노량진시장, 마포농수산물시장, 부산민락어민활어직판장, 소래포구종합어시장, 수원농수산물시장, 안양평촌농수산물시장, 인천종합연안부두어시장
---

## **기능**

### **1. 수산물별 전체 마켓 시가 현황 시각화**
- 현재까지의 마켓별 시가를 차트로 시각화하여 사용자에게 제공합니다.
- 사용된 도구:
  - Django (백엔드)
  - Chart.js (프론트엔드 차트 시각화)

### **2. 특정 날짜와 수산물 입력 시 시장별 예측 가격 제공**
- 사용자가 날짜와 수산물을 입력하면, 각 시장의 예측 가격을 제공합니다.
- 머신러닝 모델을 호출하여 실시간 예측 결과를 표시합니다.

### **3. 특정 날짜와 시장 입력 시 수산물별 예측 가격 제공**
- 특정 시장에서 수산물별 예측 가격을 사용자에게 제공합니다.
- 날짜와 시장 정보를 기반으로 데이터 처리가 이루어집니다.

---

## 서비스 화면

![서비스 스크린샷 홈](./static/screenshot/screenshot_main.png)
![서비스 스크린샷 어종별](./static/screenshot/screenshot_fish.png)
![서비스 스크린샷 마켓별](./static/screenshot/screenshot_market.png)

---

## **설치 및 실행**

### **1. 요구 사항**
- Python 3.10 이상
- Django 4.0 이상
- Node.js (선택, 프론트엔드 개발 시 필요)

### **2. 설치 절차**
1. **프로젝트 클론**
   ```bash
   git clone https://github.com/vhf1030/pisces.git
   git fetch --all
   git checkout test
   ```

2. **가상 환경 생성 및 활성화**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **필수 패키지 설치**
   ```bash
   pip install -r requirements.txt  # todo
   ```

4. **정적 파일 로드**
   ```bash
   python manage.py collectstatic
   ```

5. **개발 서버 실행**
   ```bash
   python manage.py runserver
   ```

6. **브라우저에서 접속**
   - URL: `http://127.0.0.1:8000/`

---

## **프로젝트 구조**

```plaintext
project_pisces/
├── manage.py
├── pisces/              # 프로젝트 설정 디렉터리
│   ├── settings.py      # Django 설정 파일
│   ├── urls.py          # URL 라우팅
│
├── pisces_ml/           # 주요 앱 디렉터리
│   ├── views.py         # Django View 로직
│   ├── services/        # 주요 서비스 로직 디렉터리
│   │   ├── data_preprocessor.py  # 데이터 로드 및 전처리 클래스
│   │   └── seafood_price_predictor.py  # 수산물 예측 클래스
│   ├── models/          # 데이터 및 모델 파일 디렉터리
│   │   ├── 농어_model.pkl       # 농어 모델 파일
│   │   ├── 광어_model.pkl       # 광어 모델 파일
│   │   ├── 대게_model.pkl       # 대게 모델 파일
│   │   ├── 연어_model.pkl       # 연어 모델 파일
│   │   ├── 우럭_model.pkl       # 우럭 모델 파일
│   │   ├── 참돔_model.pkl       # 참돔 모델 파일
│   │   ├── 방어_model.pkl       # 방어 모델 파일
│   │   ├── 농어_data.csv        # 농어 데이터 파일
│   │   ├── 광어_data.csv        # 광어 데이터 파일
│   │   ├── 대게_data.csv        # 대게 데이터 파일
│   │   ├── 연어_data.csv        # 연어 데이터 파일
│   │   ├── 우럭_data.csv        # 우럭 데이터 파일
│   │   ├── 참돔_data.csv        # 참돔 데이터 파일
│   │   └── 방어_data.csv        # 방어 데이터 파일
│   └── templates/       # 템플릿 디렉터리
│       ├── base.html    # 공통 템플릿
│       ├── market_overview.html  # 시각화 페이지 템플릿
│       ├── seafood_input.html    # 수산물 예측 입력 페이지
│       ├── seafood_prediction.html  # 수산물 예측 결과 페이지
│       ├── market_input.html     # 시장 예측 입력 페이지
│       └── market_prediction.html  # 시장 예측 결과 페이지
├── static/          # 정적 파일 (CSS, JS 등)
│       ├── css/
│       │   ├── bootstrap.min.css
│       │   ├── styles.css
│       └── js/
│           ├── bootstrap.min.js
│           └── jquery-3.6.0.min.js
│
└── templates
    ├── base.html      # 공통 템플릿
    ├── footer.html    # 푸터 분리 템플릿
    ├── header.html    # 헤더 분리 템플릿
    └── pisces_ml
        ├── index.html  # 테스트 페이지
        ├── predict.html  # 테스트 페이지
        ├── market_overview.html  # 시각화 페이지 템플릿
        ├── seafood_input.html    # 수산물 예측 입력 페이지
        ├── seafood_prediction.html  # 수산물 예측 결과 페이지
        ├── market_input.html     # 시장 예측 입력 페이지
        └── market_prediction.html  # 시장 예측 결과 페이지


```

---

## **사용된 주요 기술 스택**

### **백엔드**
- Django: Python 기반 웹 프레임워크
- Django REST Framework: API 개발

### **프론트엔드**
- HTML, CSS (Bootstrap)
- JavaScript (Chart.js)

### **머신러닝**
- Python 머신러닝 라이브러리 (예: scikit-learn, XGBoost 등)
- 학습된 모델 저장 및 로드 (Pickle)

---

## **향후 개선 사항**
1. **배포 환경 준비**:
   - wanted 서버 연동
2. **사용자 친화적인 입력 인터페이스**:
   - 자동 완성 기능 추가 (시장 및 수산물 선택).
3. **예측 결과 시각화 개선**:
   - 그래프 및 차트 스타일 최적화.
4. **알림 서비스 연동**:
   - 예측 가격 알림을 위한 이메일/SMS 서비스 연동.

---

- 프로젝트 생성
```
$ django-admin startproject pisces .
$ python manage.py startapp pisces_ml
```

- 서비스 실행
```
$ python manage.py runserver
```

# ssh wanted-1@100.83.113.125

TODO:
- 1차 개발
    - 이전 가격 정보 시각화
    - ml 모델 연동
    - 원티드 서버 연동
    - 기능 테스트
    - 테스트 브랜치 생성
    - 팀원 깃 연동
    - 화면 꾸미기

- 2차 개발
    - 어종 및 마켓 동적 렌더링
    - DB 생성 및 연동
    - DB 데이터 전처리 프로세스 개발
    - 데이터 수집 API 개발 및 연동
    - 메뉴 가격 예측

    