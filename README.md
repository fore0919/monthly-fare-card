# 이달의 교통카드
> monthly-fare-card
사용자가 생년월일과 출발지/도착지 (지하철역, 버스정류장)을 입력하면 평일기준 왕복 출퇴근시 예상 교통비를 계산하는 기능을
가진 product 입니다.

- 한달 기준 주말, 국경일, 공휴일을 자동으로 제외해줍니다.
- 왕복을 기준으로 계산합니다.
- 생년월일에 따른 할인율을 계산합니다.
- 응답으로 오는 기후동행카드 데이터와 비교할 수 있습니다.


## URL
url 입력

## ERD 
![monthly-fare-card](https://github.com/fore0919/monthly-fare-card/assets/91520365/7055176f-52e8-4c92-a4fb-a696251fcecc)

## OpenAPI
사용된 OpenAPI 목록 
- [[ODsay]대중교통 정류장 검색 API](https://lab.odsay.com/guide/releaseReference#searchStation)
- [[ODsay]대중교통 길찾기 API](https://lab.odsay.com/guide/releaseReference#searchPubTransPathT)
- [[공공데이터 포털]공휴일 정보 조회 API](https://www.data.go.kr/data/15012690/openapi.do)

## Spec
- Language: `python` 3.11.5
- Database: `MySQL` 8.4.0
- Framework: `fastapi`
- CI/CD: `Github Action`
- Deploy: `Docker`, `Kubernetes`
