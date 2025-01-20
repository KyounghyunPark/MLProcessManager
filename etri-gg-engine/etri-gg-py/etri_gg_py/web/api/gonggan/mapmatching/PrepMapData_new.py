import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString, MultiLineString
from utils import Utils


def convert_shp_to_csv():

    # linkDir = "/home/gaion/Documents/ETRI_CODE/02.sample_data/04_04_Map Matching/NODELINKDATA/MOCT_LINK.shp"
    # nodeDir = "/home/gaion/Documents/ETRI_CODE/02.sample_data/04_04_Map Matching/NODELINKDATA/MOCT_NODE.shp"
    # outputFile = "/home/gaion/Documents/ETRI_CODE/model_result/MAP/new_link_data1.csv"
    linkDir = "/home/tiep/dev/gonggan/data/04_04_Map Matching/[2024-03-25]NODELINKDATA/MOCT_LINK.shp"
    nodeDir = "/home/tiep/dev/gonggan/data/04_04_Map Matching/[2024-03-25]NODELINKDATA/MOCT_NODE.shp"
    outputFile = "/home/tiep/dev/gonggan/data/04_04_Map Matching/[2024-03-25]NODELINKDATA/node_link_data.csv"

    LINK_ID = "LINK_ID"
    NODE_ID = "NODE_ID"
    GEOMETRY = "geometry"
    LINK_START = "F_NODE"
    LINK_END = "T_NODE"

    print("파일 로딩, 좌표계 변환 시작")
    rawLinkDF = gpd.read_file(linkDir, encoding="cp949").to_crs(
        "EPSG:4326",
    )  # 좌표계 wgs84변환 #euc-kr
    rawNodeDF = gpd.read_file(nodeDir, encoding="cp949").to_crs("EPSG:4326")
    print("파일 로딩, 좌표계 변환 완료")
    # print("rawLinkDF.shape : ", rawLinkDF.shape)
    # print("rawNodeDF.shape : ", rawNodeDF.shape)
    # node 데이터를 이용하여 노드 시작 및 끝 데이터 준비
    startNodeDF = rawNodeDF[[NODE_ID, GEOMETRY]].rename(
        columns={NODE_ID: LINK_START, GEOMETRY: LINK_START + "_geometry"},
    )
    endNodeDF = rawNodeDF[[NODE_ID, GEOMETRY]].rename(
        columns={NODE_ID: LINK_END, GEOMETRY: LINK_END + "_geometry"},
    )

    # 시작과 끝 노드를 연결
    linkStartNodeDF = rawLinkDF[
        ["geometry", "LINK_ID", "F_NODE", "T_NODE", "ROAD_NAME", "MAX_SPD"]
    ].merge(startNodeDF, on=LINK_START)
    linkNodeJoinDF = linkStartNodeDF.merge(endNodeDF, on=LINK_END)
    # print("linkNodeJoinDF.shape : ",linkNodeJoinDF.shape)

    # 간단하게 테스트 위해 50개만 처리
    # linkNodeJoinDF = linkNodeJoinDF.iloc[0:50].copy()

    """-------------------------일단 여기까지는 완료-------------------------------------"""

    def create_geometry_list(row):
        # CoordinateSequence 객체의 좌표를 리스트로 변환
        start_point = list(row[LINK_START + "_geometry"].coords)  # Point -> [(x, y)]
        end_point = list(row[LINK_END + "_geometry"].coords)  # Point -> [(x, y)]

        line = row["geometry"]
        try:
            if isinstance(line, LineString):
                line_coords = list(line.coords)  # LineString -> [(x1, y1), (x2, y2)]
                answer = start_point + line_coords + end_point
                return answer
            elif isinstance(line, MultiLineString):
                multi_line_coords = [
                    list(m.coords) for m in line.geoms
                ]  # MultiLineString -> [[(x1, y1), (x2, y2)], ...]
                answer = (
                    start_point
                    + [coord for line in multi_line_coords for coord in line]
                    + end_point
                )
                return answer
        except:
            print("error")

    # 이 부분 Process finished with exit code 137 (interrupted by signal 9:SIGKILL) 에러 발생 가능성 있음 나눠서 처리하는 코드 필요
    linkNodeJoinDF.loc[:, "geometry"] = linkNodeJoinDF.apply(
        create_geometry_list,
        axis=1,
    )

    link_segments = []
    print("전처리 진행 중 ~~~!")
    for _, row in linkNodeJoinDF.iterrows():
        link_id = row[LINK_ID]
        road_name = row["ROAD_NAME"]
        speed_limit = row["MAX_SPD"]
        gps_arrs = row["geometry"]
        # print(2,gps_arrs)
        # print(3,gps_arrs[0])

        for i in range(
            len(gps_arrs) - 1,
        ):  # gps_arrs[0]은 시작점이므로 제외 gps_arr (x,y) 형태
            start_point = gps_arrs[i]
            end_point = gps_arrs[i + 1]

            start_point_x = start_point[0]
            start_point_y = start_point[1]

            end_point_x, end_poiny_y = (lambda x: (x[0], x[1]))(end_point)
            # end_point_x= end_point[0],  # line loop x #간단하게 안 됨 그래서 람다로 변환
            # end_poiny_y= end_point[1],  # line loop y

            # 여기 아래에 제한속도 도로이름 추가해야함
            link_segments.append(
                [
                    link_id,
                    start_point_x,  # start point x
                    start_point_y,  # start point y
                    end_point_x,  # line loop x
                    end_poiny_y,  # line loop y
                    road_name,
                    speed_limit,
                    Utils.get_mesh_total(start_point_x, start_point_y),
                    Utils.get_mesh_total(end_point_x, end_poiny_y),
                ],
            )

    print("최종 반환 갯수", len(link_segments))
    print("파일 저장 중")

    link_segments_df = pd.DataFrame(
        link_segments,
        columns=[
            "linkId",
            "x1",
            "y1",
            "x2",
            "y2",
            "road_name",
            "speed_limit",
            "mesh1",
            "mesh2",
        ],
    )
    link_segments_df.to_csv(outputFile, index=False, encoding="utf-8")

    print("변환 완료!")


if __name__ == "__main__":
    convert_shp_to_csv()
