import heapq
import math
from collections import defaultdict

from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.base import ControllerBase
from app.models.station import StationLine
from app.modules.transit import Transit
from app.utils.exception import InvalidValueError


class PoiController(ControllerBase):
    async def get_payment_by_poi(
        self,
        start: str,
        end: str,
        start_station_type: str,
        end_station_type: str,
    ) -> tuple[int, float]:
        transit = Transit()
        start_lng, start_lat = await transit.get_coordinate_by_station_name(
            station_name=start, station_type=start_station_type
        )
        end_lng, end_lat = await transit.get_coordinate_by_station_name(
            station_name=end, station_type=end_station_type
        )
        fare, distance = await transit.get_payment_by_coordinate(
            sx=start_lng, sy=start_lat, ex=end_lng, ey=end_lat
        )
        return fare, distance

    async def get_payment_by_distance(
        self,
        session: AsyncSession,
        start: str,
        end: str,
    ) -> tuple[int, float]:
        station_lines = await self.daos.v1.station.get_station_lines(
            session=session
        )
        station_name_to_id = {}
        for sl in station_lines:
            if sl.station and sl.station.station_name not in station_name_to_id:
                station_name_to_id[sl.station.station_name] = sl.station_id

        departure_id = station_name_to_id.get(start)
        arrival_id = station_name_to_id.get(end)
        if departure_id is None or arrival_id is None:
            raise InvalidValueError("역 정보를 찾을 수 없습니다.")

        graph = self._build_graph(
            station_lines=station_lines, transfer_cost=0.0
        )

        start_nodes = [
            (sl.station_id, sl.line_id)
            for sl in station_lines
            if sl.station_id == departure_id
        ]

        shortest_distance, path = self._dijkstra(graph, start_nodes, arrival_id)
        print("최단거리:", shortest_distance)
        print("경로 (station_id, line_id):", path)
        fare = self._calculate_fare(shortest_distance)
        return fare, shortest_distance

    def _calculate_fare(
        self, distance: float, transfer_applied: bool = False
    ) -> int:
        """
        지하철 요금 정책:
          - 10km 이내: 기본요금 1,400원
          - 10km 초과 ~ 50km 이내: 10km 초과한 거리에 대해 5km마다 100원 추가
          - 수도권 내/외 구간을 연속 이용하는 경우: 추가 100원
        매개변수:
          distance: 최단 거리 (km)
          transfer_applied: 수도권 내/외 연속 이용 여부 (True이면 추가 100원 적용)
        """
        base_fare = 1400

        if distance <= 10:
            fare = base_fare
        elif distance <= 50:
            additional_units = math.ceil((distance - 10) / 5)
            fare = base_fare + additional_units * 100
        else:
            additional_units = math.ceil((50 - 10) / 5)
            fare = base_fare + additional_units * 100

        if transfer_applied:
            fare += 100

        return fare

    def _build_graph(
        self, station_lines: list[StationLine], transfer_cost: float = 0.0
    ) -> dict[tuple[int, int], list[tuple[tuple[int, int], float]]]:
        """
        - 노드: (station_id, line_id) 튜플
        - 엣지: 동일 노선 내 인접 역 간의 거리 (distance_from_prev)
                동일 역에서 다른 노선 간 환승 비용 (transfer_cost)
        :return: 노드와 엣지 가중치로 구성된 그래프 (딕셔너리)
        """
        graph = defaultdict(list)
        lines_by_line = defaultdict(list)
        # 노선 id를 키값으로 가진 dict에 station 오브젝트를 list로 할당 {line_id: [StationLine, ...]}
        for sl in station_lines:
            lines_by_line[sl.line_id].append(sl)
        for line_id, sl_list in lines_by_line.items():
            # 각 노선별 역 순서(sequence) 정렬
            sl_list.sort(key=lambda sl: sl.sequence)
            for i in range(1, len(sl_list)):
                prev = sl_list[i - 1]
                curr = sl_list[i]
                weight = (
                    curr.distance_from_prev
                    if curr.distance_from_prev is not None
                    else 0.0
                )
                prev_node = (
                    prev.station_id,
                    prev.line_id,
                )  # 이전역(노드) 역id, 노선id
                curr_node = (
                    curr.station_id,
                    curr.line_id,
                )  # 현재역(노드) 역id, 노선id
                graph[prev_node].append(
                    (curr_node, weight)
                )  # {(1,1): [((2,0), 1.0)]}
                graph[curr_node].append(
                    (prev_node, weight)
                )  # {(2,1): [((2,0), 1.0)]}
        # 같은 역에 속한 다른 노선 간 환승 연결 (환승 비용 추가)
        station_to_nodes = defaultdict(list)
        for sl in station_lines:
            node = (sl.station_id, sl.line_id)
            station_to_nodes[sl.station_id].append(
                node
            )  # [(1,1),(1,4)] : id가 1인 서울역에 속한 노선이 1호선과 4호선
        for station, nodes in station_to_nodes.items():
            for i in range(len(nodes)):
                for j in range(i + 1, len(nodes)):
                    prev_node = nodes[i]
                    curr_node = nodes[j]
                    graph[prev_node].append((curr_node, transfer_cost))
                    graph[curr_node].append((prev_node, transfer_cost))
                    # graph = {(2,1) : [((1, 1), Decimal('1.10')), ((3, 1), Decimal('1.00')), ((2, 2), 0.0), ((2, 2), 0.0)] ...}
                    # id=2(시청역), 1호선 : (id=1(서울역), 1호선) 거리 1.1, (id=3(종각역), 1호선) 거리 1.0, (id=2(시청역), 2호선) 환승비용 0.0...
        return graph

    def _dijkstra(
        self,
        graph: dict[tuple[int, int], list[tuple[tuple[int, int], float]]],
        start_nodes: list[tuple[int, int]],
        goal_station: int,
    ) -> tuple[float, list[tuple[int, int]]]:
        """
        Dijkstra 알고리즘을 사용해 여러 출발 노드에서 목표 노드 까지 최단 거리 계산

        :param graph: 노드와 엣지 가중치로 구성된 그래프 (딕셔너리)
        :param start_nodes: 출발역에 해당하는 노드들의 리스트 (튜플)
        :param goal_station: 도착역의 station_id
        :return: (최단 거리, 경로 (노드 튜플 리스트))
        """
        dist: dict[tuple[int, int], tuple[int, float]] = {}
        prev = {}
        heap = []
        for node in start_nodes:
            dist[node] = (0, 0.0)
            heapq.heappush(heap, (0, 0.0, node))
        goal_node = None
        while heap:
            trans, cur_dist, u = heapq.heappop(heap)
            if (trans, cur_dist) > dist[u]:
                continue
            if u[0] == goal_station:
                goal_node = u
                break
            for v, weight in graph.get(u, []):
                additional_transfer = (
                    1 if (u[0] == v[0] and u[1] != v[1]) else 0
                )
                new_trans = trans + additional_transfer
                new_dist = cur_dist + float(weight)
                new_cost = (new_trans, new_dist)
                if v not in dist or new_cost < dist[v]:
                    dist[v] = new_cost
                    prev[v] = u
                    heapq.heappush(heap, (new_trans, new_dist, v))
        if goal_node is None:
            return float("inf"), []
        path = []
        node = goal_node
        while node in prev:
            path.append(node)
            node = prev[node]
        path.append(node)
        path.reverse()
        final_distance = math.floor(dist[goal_node][1] * 100) / 100
        return final_distance, path
