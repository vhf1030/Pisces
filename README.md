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




# TODO
- 1차 개발
    - 모델 학습에는 전체 마켓의 피쳐가 사용되어야 함
    - 최종 데이터 생성 스크립트 코드 저장
    - 데이터 파일 및 모델 파일 생성
    - 서비스 연동

- 2차 개발
    - DB 생성 및 연동
    - DB 데이터 전처리 프로세스 개발
    - 데이터 수집 API 개발 및 연동
