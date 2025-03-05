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
- 예상 할인 요금을 확인하고 기후동행 카드요금과 비교할 수 있습니다.
- 경로 데이터는 front가 없는 관계로 가장 첫번째 경로를 불러옵니다. (TMAP API 이용)
  - 지하철, 버스 등 종류를 선택하지 않으면 정확도가 떨어질 수 있습니다.
"""

tags_metadata = [
    {
        "name": "[v1] Best Card",
        "description": "교통카드 추천",
    }
]

fare_card_v2 = """
### 위의 API와 동일한 기능을 가지고 있으나, 경로 데이터를 DB에서 불러옵니다.

- 역 정보, 역간 거리, 노선 정보 등은 OPEN DATA를 이용합니다.
  - 1~8호선간의 이동 경로만 조회가 가능합니다.
- 다익스트라 알고리즘을 이용해 최단거리와 요금을 계산합니다
  - 위의 API와 요금, 이동 거리의 정확도를 비교해볼 수 있습니다.
"""
