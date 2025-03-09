# 이달의 교통카드
> 🚀 Swagger Link: [monthly-fare-card](https://port-0-monthly-fare-card-lxvf8lgx584ba9bc.sel5.cloudtype.app/docs#/)

</br>

## 1. Introduction
사용자가 생년월일과 출발지/도착지 (지하철역, 버스정류장)을 입력하면 평일기준 왕복 출퇴근시 예상 교통비를 계산하는
기능을 가진 토이 프로젝트 입니다.

</br>

## 2. Description

📌 **[GET]**`v1/best-card/`
- `TMAP API`를 이용해 역명으로 좌표를 검색하고 해당 좌표로 대중교통 길찾기 API를 호출해 응답받은 데이터를 가공해서 데이터를 반환합니다. 

📌 **[GET]**`v1/best-card/db`
- 역간거리 및 소요시간 정보 `OPEN DATA`를 DB에 저장 후 `다익스트라 알고리즘`을 적용해 직접 최단거리와 요금을 계산하는 API를 추가했습니다.위의 API에서 응답하는 데이터와 비교해볼 수 있습니다.
- 데이터가 1~8호선 정보밖에 제공하지 않으므로 해당 노선안에서 이동하는 경로만 제공합니다.

📌 **[공통]**
- 한달 기준 주말, 국경일, 공휴일을 자동으로 제외해줍니다.
- 왕복을 기준으로 계산합니다.
- 생년월일에 따른 할인율을 계산합니다.
- 응답으로 오는 기후동행카드 데이터와 비교할 수 있습니다.

  
</br>

## 3. ERD 
![monthly-fare-card (1)](https://github.com/user-attachments/assets/4aa26dcb-624b-43fe-b7b7-e5b31cb1120f)


</br>

## 4. OpenAPI
사용된 OpenAPI 목록 
- [[TMAP]대중교통 정류장 검색 API](https://tmap-skopenapi.readme.io/reference/%EC%9E%A5%EC%86%8C%ED%86%B5%ED%95%A9%EA%B2%80%EC%83%89)
- [[TMAP]대중교통 길찾기 API](https://transit.tmapmobility.com/sample/routes)
- [[공공데이터 포털]공휴일 정보 조회 API](https://www.data.go.kr/data/15012690/openapi.do)
- [[서울교통공사] 역간거리 및 소요시간 정보 OPEN DATA](https://data.seoul.go.kr/dataList/OA-12034/S/1/datasetView.do)
</br>

## 5. Spec
- Language: `python` 3.11.5
- Database: `MySQL` 8.4.0 by `Kubernetes` (local) / `MariaDB` 11.2 (prod)
- Framework: `fastapi`
- Deploy: `CloudType`
- CI/CD: `Github Action`
</br>

## 6. 회고

> 현재는 ODsayAPI를 사용하지 않습니다.

**📌 ODsayAPI 사용 시 서버 공인 IP 문제** 

`문제`
- 타 OPENAPI는 대부분 해당 사이트에 도메인을 등록하고 발급받은 API_KEY를 통해 호출 했던 경험이 있습니다.
- 해당 API는 프론트가 아닌 서버 단에서 호출할 경우 서버의 공인 IP를 등록해야 API_KEY를 인식해서 호출이 가능한 로직 입니다.

`해결`
- 포트포워딩이 불가능하기 때문에 공공장소에서 작업 불가 -> 배포해서 고정 IP를 가지기 전까지는 집에서 작업하는 방향으로 해결했습니다.
- 집의 공유기 게이트웨이 설정에서 내부IP와 공인IP를 포트포워딩 후 등록해서 사용했습니다.
- 배포 이후에는 클라우드타입 서버의 아웃바운드 IP를 등록해 사용했습니다.

</br>

**📌 아쉬운 점**

1. `프론트의 부재`
   
   백엔드로만 개발을 해야하는 상황이다 보니 스웨거 기준으로 API 하나에 최대한 사용하기 편리하도록 구성했는데    
   프론트가 있었더라면 좀 더 사용자가 원하는 유효한 결과를 도출하고 (`ex` 역/터미널명 조회 및 경로 조회 )     
   고도화를 할 수 있었을 것 같아서 그 부분이 아쉬운 점으로 남습니다.   

2. `인프라 관련`

   AWS 프리티어 기간 만료로 EKS나 RDS를 이용해 배포 할수 없었고   
   단일 서비스다 보니 현업에서 이용했던 `istio`를 적용해보지 못한게 아쉽습니다.    
   따라서 무료로 사용할 수 있는 [클라우드 타입](https://docs.cloudtype.io/guide/welcome/before-using#-9)을 채택 했으며 사이즈가 작은 서비스에 사용하기 편리한 점이 매우 좋았습니다    
