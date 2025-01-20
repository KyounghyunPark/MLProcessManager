import pandas as pd

from etri_gg_py.web.api.gonggan.mapmatching.utils import Utils

utilsfunc = Utils()


def do_map_matching(taxi_df: pd.DataFrame, link_df: pd.DataFrame) -> pd.DataFrame:
    VEHICLE_COL = "vehicle"
    MAX_CAR_PER_PART = 20

    # 아래 코드는 차량별로 데이터를 나누어서 처리하는 코드 판다스의 groupby를 사용하면 더 간단하게 처리할 수 있음
    # taxi_partitions = partition_data_into_multiple_df(taxi_df, MAX_CAR_PER_PART, VEHICLE_COL)

    # 판다스에서는 간단하게 groupby를 사용하여 처리할 수 있음
    # matching_results = taxi_df.head(5).groupby(VEHICLE_COL).apply(grouby_method, link_df)     #groupby를 사용하여 자동차별로 데이터를 나누어 처리
    """여기도 수정함 아래와 같이 움직여야 함"""
    (
        taxi_df["link_id"],
        taxi_df["road_name"],
        taxi_df["speed_limit"],
        taxi_df["car2LinkMinDistance"],
    ) = zip(*taxi_df.apply(grouby_method, link_df=link_df, axis=1))
    return taxi_df
    # 테스트 위해 5개만 처리
    # subset = taxi_df.head(5).copy()
    # subset['link_id'], subset['car2LinkDistance'] = zip(*subset.apply(grouby_method, link_df=link_df, axis=1))
    # return subset


def grouby_method(row, link_df):

    lng = row["x_wgs84"]
    lat = row["y_wgs84"]
    mesh_id = row["mesh"]
    carGPS = utilsfunc.point2d(lng, lat)

    res = findNearestLink(
        link_df,
        carGPS,
        mesh_id,
    )  # carGPS와 mesh id 값은 taxi_df에 있는 값
    return res


# 해당 택시의 gps와 mesh_id를 받아서 같은 mesh 내 가장 가까운 링크를 찾는 함수
def findNearestLink(link_df, carPoint, mesh_id):

    matched_link_df = link_df[
        (link_df["mesh1"] == mesh_id) | (link_df["mesh2"] == mesh_id)
    ].copy()  # 링크데이터 프레임에서 mesh가 같은 데이터만 추출

    # 일치하는 링크의 갯수
    error = 1

    # 정확히 매칭되는 링크가 없다면, 검색 범위를 확장(링크값에 +error or -error)하여 계속 시도
    while matched_link_df.empty:
        print(
            "No exact matched link for meshID %d with gps (%f, %f)".format(),
        )
        matched_link_df = link_df[
            (
                (link_df["mesh1"] <= (mesh_id + error))
                & (link_df["mesh1"] >= (mesh_id - error))
            )
            | (
                (link_df["mesh2"] <= (mesh_id + error))
                & (link_df["mesh2"] >= (mesh_id - error))
            )
        ].copy()
        error += 1
    # 링크가 있으면 탈출
    # 여기가 query_result를 apply로 변경한 코드 해당 링크 중 가장 가까운 링크를 찾는 코드

    matched_link_df["distance"] = matched_link_df.apply(
        lambda row: utilsfunc.get_distance_point_to_line_in_m(  # 점과 선분 사이의 거리를 계산하는 함수
            utilsfunc.point2d(row["x1"], row["y1"]),
            utilsfunc.point2d(row["x2"], row["x2"]),  # y2가 아닌 x2 사용
            carPoint,
        ),
        axis=1,
        # 여기서 스칼라는 링크아이디 추가하네
    )

    # 가장 최단거리의 로우를 반환하고 그 로우의 linkId와 distance를 반환
    if not matched_link_df.empty:
        min_distance_row = matched_link_df.loc[
            matched_link_df["distance"].idxmin()
        ]  # 가장 가까운 거리의 로우를 찾음
        # return utilsfunc.matching_result(int(min_distance_row['linkId']), min_distance_row['distance'])  # 여기서 linkId와 ,
        """ 여기 수정함 여기 수정해서 위에도 같이 수정"""
        return utilsfunc.matching_result2(
            int(min_distance_row["linkId"]),
            min_distance_row["road_name"],
            min_distance_row["speed_limit"],
            min_distance_row["distance"],
        )  # 해당 로우의 linkId와 road_name, speed_limit를 반환

    return None


# 차량별로 데이터를 나누어 처리하는 함수 (차량 수가 많을 경우, 메모리 문제를 해결하기 위해 사용) 스파크에서 쓴 코드 옮겼
# def partition_data_into_multiple_df(taxi_df, max_car_per_part: int, car_id_col: str) -> list:
#     distinct_car = taxi_df[car_id_col].drop_duplicates()
#     car_count = len(distinct_car) # 중복 제거한 고유 차량 수
#     print("Distinct number of car", car_count)
#
#     car_list = sorted(distinct_car.tolist())
#     cc = 0
#     new_car_list = []
#     part_list = []
#
#     for index in range(car_count):
#         part_list.append(car_list[index])
#         cc += 1
#         if cc > max_car_per_part:
#             new_car_list.append(part_list)
#             cc = 0
#             part_list = []
#
#     new_car_list.append(part_list)
#
#     taxi_df_list = []
#     for part_list in new_car_list:
#         query = " | ".join([f"{car_id_col} == '{car}'" for car in part_list])
#         taxi_df_list.append(taxi_df.query(query).copy())
#
#     return taxi_df_list

# def do_map_matching_v3(taxi_df, link_df):
#     import pandas as pd
#     import numpy as np
#
#     def point2line_dist(x_wgs84, y_wgs84, vtx_1, vty_1, vtx_2, vty_2):
#         car_point = np.array([x_wgs84, y_wgs84])
#         start_point = np.array([vtx_1, vty_1])
#         end_point = np.array([vtx_2, vty_2])
#         line_vec = end_point - start_point
#         point_vec = car_point - start_point
#         line_len = np.linalg.norm(line_vec)
#         line_unitvec = line_vec / line_len
#         point_vec_scaled = point_vec / line_len
#         t = np.dot(line_unitvec, point_vec_scaled)
#         t = np.clip(t, 0, 1)
#         nearest = start_point + t * line_vec
#         dist = np.linalg.norm(nearest - car_point)
#         return dist
#
#     taxi_df['key'] = taxi_df['mesh1'].astype(str) + '_' + taxi_df['mesh2'].astype(str)
#     link_df['key'] = link_df['mesh1'].astype(str) + '_' + link_df['mesh2'].astype(str)
#     matched_link_df = pd.merge(taxi_df, link_df, on='key')
#
#     matched_link_df['dist'] = matched_link_df.apply(
#         lambda row: point2line_dist(row['x_wgs84'], row['y_wgs84'], row['x1'], row['y1'], row['x2'], row['y2']), axis=1)
#
#     reduce_df = matched_link_df.loc[matched_link_df.groupby('id')['dist'].idxmin()]
#     reduce_df = reduce_df[['dist', 'vehicle', 'date', 'month_created', 'area_code', 'x_bessel', 'y_bessel', 'status', 'company_code', 'driver_ID', 'x_wgs84', 'y_wgs84', 'linkId']]
#
#     return reduce_df
