# My ML Project

## 📖 프로젝트 소개
**My ML Project**는 머신러닝을 활용하여 해산물 가격을 예측하는 서비스입니다.  
소비자에게 최적의 구매 시점을 제공하여 경제적 이득을 제공합니다.

---

## 🚀 주요 기능
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
    - 데이터 수집 API 개발 및 연동
