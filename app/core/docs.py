description = """
## 교통 카드 추천 API
`description`: 사용자가 생년월일과 출발지/도착지 (지하철역, 버스정류장)을 입력하면 평일기준 왕복 출퇴근시 예상 교통비를 계산하는 기능을 가진 product 입니다.
</br>
</br>
`github_link` : [https://github.com/fore0919/monthly-fare-card](https://github.com/fore0919/monthly-fare-card)
"""
fare_card = """
### 평균 한달 출근 시 교통카드 할인금액을 계산하는 API

- 주말, 국경일, 대체공휴일은 제외한 평일만 계산 (공공데이터API 이용)
- 왕복 기준
- 기후동행 카드와 비교
- 경로 데이터는 지하철-지하철 환승이 우선합니다.
- 지하철의 경우 "역" 단어는 제외한 단어를 검색해주세요.
  - 입력예시: 강남역(X), 강남(O)
"""

tags_metadata = [
    {
        "name": "[v1] Best Card",
        "description": "교통카드 추천",
    },
]
