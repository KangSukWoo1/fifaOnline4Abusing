# fifaOnline4Abusing
fifaOnline4에서 일어나는 거래 중 BP 거래가 의심되는 계정에 관한 추적 알고리즘입니다.

관련 포트폴리오 Notion : https://innovative-alligator-2f6.notion.site/4-4573409b18fb451686af2035b63f6fd0?pvs=4


데이터 적재
- fifaOnlineExecutor.py <br>
실행 파일
- - nickNameCrawling.py <br>
피파 공식 홈페이지에서 닉네임 크롤링, API 활용하여 거래 데이터 수집
- - bigqueryUpsert.py <br>
가져온 데이터를 전처리하여 bigquery에 upsert

전처리 및 모델링
- RandomForest_train.py <br>

거래가 짧은 시간동안, 많은 이득을 본 매물들
그리고 외부 요인(챔스, 신규시즌 등)의 영향이 없을 것이라 판단되는 매물들을 위주로 선별함

전처리 및 RandomForest활용하여 모델링 진행
- RandomForest_validation.py <br>
validation set에 테스트

![image](https://github.com/KangSukWoo1/fifaOnline4Abusing/assets/58423399/2d52feb5-0314-40b3-8129-9e88cf24444e)
---
의심 매물 리스트 ![image](https://github.com/KangSukWoo1/fifaOnline4Abusing/assets/58423399/b9f2ca3a-dd53-4047-bf29-24323d0394e4)

