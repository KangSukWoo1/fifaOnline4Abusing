# fifaOnline4Abusing
fifaOnline4에서 일어나는 거래 중 BP 거래가 의심되는 계정에 관한 추적 알고리즘입니다.



데이터 적재
- fifaOnlineExecutor.py 
실행 파일
- - nickNameCrawling.py 
피파 공식 홈페이지에서 닉네임 크롤링, API 활용하여 거래 데이터 수집
- - bigqueryUpsert.py 
가져온 데이터를 전처리하여 bigquery에 upsert

전처리 및 모델링
- RandomForest_train.py
전처리 및 RandomForest활용하여 모델링 진행
- RandomForest_validation.py 
validation set에 테스트
