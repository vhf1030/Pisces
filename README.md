# 🐟 PISCES – 수산물 가격 예측 서비스

## 📌 프로젝트 개요
**PISCES**는 머신러닝을 활용하여 수산물 가격을 예측하고, 소비자에게 **최적의 구매 시점**을 제공하는 웹 기반 서비스입니다.

- **예측 대상 어종**: 광어, 농어, 대게, 연어, 우럭, 참돔, 방어  
- **시장 범위**: 가락시장, 노량진시장, 구리농수산물시장 등 전국 주요 10개 수산시장  
- **데이터**: 수산물 가격, 기상 정보, 환율, 네이버 검색 트렌드 등 복합 데이터 활용

👉 [📁 GitHub Repository](https://github.com/vhf1030/ml_pisces)

---

## ⚙️ 주요 기능

### ✅ 1. 어종별 시장 시가 현황 시각화  
- 현재까지의 시장별 시가를 차트로 제공하여 비교 가능  
- `Chart.js`를 활용한 직관적인 시각화

### ✅ 2. 날짜 + 어종 입력 시 시장별 가격 예측  
- 입력된 날짜와 어종에 대해 각 시장의 예측 가격을 제공  
- 머신러닝 모델을 통한 실시간 예측

### ✅ 3. 날짜 + 시장 입력 시 어종별 가격 예측  
- 특정 시장에 대한 수산물별 가격을 예측하여 제공

---

## 🖥️ 기술 스택

| 구분 | 기술 |
|------|------|
| 언어 | Python |
| 모델링 | Scikit-learn, LightGBM |
| 웹 프레임워크 | Django |
| 데이터 시각화 | Seaborn, Chart.js |
| 협업 도구 | Git, Notion |
| 배포 예정 | Docker, SQLite (1차 개발은 파일기반) |

---

## 🖼️ 서비스 화면

### 수산물 가격 예측
![서비스 스크린샷 홈](./project_pisces/static/screenshot/screenshot_main.png)

### 어종별 시장 가격 예측
![서비스 스크린샷 어종별](./project_pisces/static/screenshot/screenshot_fish.png)

### 시장별 수산물 가격 예측
![서비스 스크린샷 마켓별](./project_pisces/static/screenshot/screenshot_market.png)

---

## 🚀 진행 과정
1. **데이터 전처리**: 기상 데이터, 검색 트렌드, 수산물 가격 데이터를 정리 및 분석.
2. **모델 학습**: 머신러닝 모델을 통해 가격 예측 수행.
3. **결과 시각화**: 예측된 데이터를 그래프 및 표로 제공.

---

## 서비스
# Pisces ML: 수산물 가격 예측 서비스

Pisces ML은 10개의 마켓과 7종의 수산물을 대상으로 한 머신러닝 기반 수산물 가격 예측 웹 애플리케이션입니다. 이 프로젝트는 사용자가 원하는 날짜, 수산물, 시장 정보를 기반으로 예측 가격을 제공하고, 현재까지의 시장 시가를 시각화하는 기능을 제공합니다.
- 어종 리스트: 농어, 광어, 대게, 연어, 우럭, 참돔, 방어
- 시장 리스트: 가락시장, 강서농수산물시장, 구리농수산물시장, 노량진시장, 마포농수산물시장, 부산민락어민활어직판장, 소래포구종합어시장, 수원농수산물시장, 안양평촌농수산물시장, 인천종합연안부두어시장

---


## 🛠️ 설치 및 실행 방법


### git setting
$ git clone https://github.com/vhf1030/ml_pisces.git

(주의) 개인 장비로 작업할 때에만 설정합니다
$ git config --global user.name "YourName"
$ git config --global user.email "YourEmail@example.com"


### 자주쓰는 git 명령어
- commit 내역 확인
$ git log

- 현재 파일 변경 상태 확인
$ git status

- 파일 변경 내용 확인
$ git diff

- 특정 파일의 수정 내용을 마지막 커밋으로 되돌리기
$ git restore [파일경로]
ex. git restore notebooks/eda_ikh.ipynb
(주의) 수정한 내용이 사라집니다


### git 규칙
1. git pull 진행 후 작업
- merge 메세지가 뜨는 경우 ":q" 입력
2. 브랜치는 따로 구분하지 않음 - 번거로우니까

### 서버 접속 (교육장 내에서)
$ ssh wanted-1@192.168.10.96

### 글로벌 세팅 없이 커밋 / 푸시 하는 방법 (서버에서 작업할 때 필요)
git -c user.name="YourName" -c user.email="YourEmail@example.com" add .
git -c user.name="YourName" -c user.email="YourEmail@example.com" commit -m "커밋 메시지"
git -c user.name="YourName" -c user.email="YourEmail@example.com" push


서비스 개발: https://github.com/vhf1030/pisces

- 1차 개발
    - 서비스용 스크립트 디렉터리 관리 - EDA와 구분
    - 데이터 수집 및 모델 성능 평가 내용 정리
    - 모델 학습에는 전체 마켓의 피쳐가 사용되어야 함 - 노량진 시장 평균가격으로 전처리
    - 최종 데이터 생성 스크립트 코드 저장
    - 데이터 파일 및 모델 파일 생성 - pkl 파일 생략
    - 서비스 연동

# TODO
- 2차 개발
    - DB 생성 및 연동
    - DB 데이터 전처리 프로세스 개발
    - 주기적 데이터 수집 API 개발 및 연동
