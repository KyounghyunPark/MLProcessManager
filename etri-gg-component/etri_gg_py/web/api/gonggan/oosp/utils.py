import math

import numpy as np
import pandas as pd


class Utils:
    def __init__(self):
        pass

    def point2d(self,x,y):
        return (x,y)

    def matching_result(self,link_id, distance):
        return (link_id, distance)

    #여기서부터 아래 3개 함수는 map_matcher(OOSP).py findNearestLink 함수에서 사용되는 함수들
    def get_distance_point_to_line_in_m(self, p, line_start, line_end): #데이터 넣을 떄는 start,end, car 순으로 넣음
        # 선분과 점 사이의 거리 계산
        length = self.get_distance_in_m(line_start, line_end)
        triangle_area = self.get_triangle_area(p, line_start, line_end)

        try:
            # 선분과 점 사이의 거리 계산
            return 2 * triangle_area / length
        except:
            return 0



    def get_distance_in_m(self,p1, p2):
        lat1, lng1 = p1[1], p1[0]
        lat2, lng2 = p2[1], p2[0]

        # 지구 반지름 (미터 단위)
        earth_radius = 6371000

        # 위도와 경도의 차이를 라디안으로 변환
        dlat = math.radians(lat2 - lat1)
        dlng = math.radians(lng2 - lng1)

        # Haversine 공식을 사용하여 두 점 간의 거리 계산
        a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(
            dlng / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        dist = earth_radius * c
        return dist

    def get_triangle_area(self, p0, p1, p2):
        # 삼각형의 세 변 길이 계산
        d0 = self.get_distance_in_m(p0, p1)
        d1 = self.get_distance_in_m(p1, p2)
        d2 = self.get_distance_in_m(p2, p0)

        # 반둘레 (semi-perimeter)
        half_p = (d0 + d1 + d2) / 2

        # 헤론의 공식을 사용하여 삼각형의 면적 계산
        try:
            area = math.sqrt(half_p * (half_p - d0) * (half_p - d1) * (half_p - d2))
        except:
            area = 0
        return area

    @staticmethod
    def get_mesh_total(x, y) -> int:
        x = float(x)
        y = float(y)
        n_x = np.floor(x * 10.0) / 10.0
        n_y = np.floor(y * 10.0) / 10.0
        return int((n_y - 33.0) * 530 + (n_x - 125.8) * 10)


def main():
    # 파일 경로 설정
    link_dir = "D:/project/GongganBigdata/5thYearFunctions/One_One_shortest_path/UTMK/link_wgs84.csv"
    node_dir = "D:/project/GongganBigdata/5thYearFunctions/One_One_shortest_path/UTMK/node_wgs84.csv"
    output_file = "alink/link_big_mesh_old.csv"

    # Shape 파일 읽기
    raw_link_df = Utils.shape_to_df(link_dir)
    print(raw_link_df.head())

    raw_node_df = Utils.shape_to_df(node_dir)
    print(raw_node_df.head())

    # 시작 및 종료 노드 DataFrame 준비
    start_node_df = raw_node_df.rename(columns={"NODE_ID": "F_NODE", "geometry": "F_NODE_geometry"})[["F_NODE", "F_NODE_geometry"]]
    end_node_df = raw_node_df.rename(columns={"NODE_ID": "T_NODE", "geometry": "T_NODE_geometry"})[["T_NODE", "T_NODE_geometry"]]

    # 링크 노드 조인
    link_start_node_df = pd.merge(raw_link_df, start_node_df, on="F_NODE")
    link_node_join_df = pd.merge(link_start_node_df, end_node_df, on="T_NODE")

    # geometry 결합
    link_node_join_df["geometry"] = link_node_join_df["F_NODE_geometry"] + link_node_join_df["geometry"] + link_node_join_df["T_NODE_geometry"]

    # 라인 문자열을 배열로 변환
    link_node_join_df["geometry"] = link_node_join_df["geometry"].apply(Utils.line_str_to_mesh_str)

    # 최종 데이터 생성
    final_data = []

    for _, row in link_node_join_df.iterrows():
        link_id = row["LINK_ID"]
        mesh_arr = row["geometry"]
        final_data.append((link_id, mesh_arr))

    # DataFrame으로 변환
    final_df = pd.DataFrame(final_data, columns=["LINK_ID", "MESH_ARRAY"])

    print(final_df.head())
    Utils.save_df(final_df, output_file)

    print("Map Data processing completed!")

if __name__ == "__main__":
    main()
