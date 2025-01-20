from pathlib import Path

import chardet
import pandas as pd

from etri_gg_py.web.api.gonggan.mapmatching import map_matcher
from etri_gg_py.web.api.gonggan.mapmatching.utils import Utils
from etri_gg_py.web.lifespan import DATA_BIG_INPUT, DATA_INPUT, DATA_OUTPUT, global_var

utilsfunc = Utils()


class MapMatching:
    @staticmethod
    def main():
        # args
        taxi_file = (
            "/home/tiep/dev/gonggan/data/04_04_Map Matching/MapMatching_input.csv"
        )
        link_dir = "/home/tiep/dev/gonggan/data/04_04_Map Matching/new_link_data.csv"
        output_file = "/home/tiep/dev/gonggan/data/04_04_Map Matching/MapMatching_output_by_document2.csv"
        select_col = "vehicle,date,month_created,area_code,x_bessel,y_bessel,status,company_code,driver_ID,x_wgs84,y_wgs84"

        # 파일 인코딩 확인

        # If input arguments are provided, use them
        # taxi_file = sys.argv[1]
        # link_dir = sys.argv[2]
        # output_file = sys.argv[3]
        # select_col = sys.argv[4]

        taxi_col = select_col.split(",")  # 문자열 -> 리스트

        # Load link data
        link_df = pd.read_csv(link_dir, encoding="utf-8")

        # 택시 관련 데이터 전처리 작업 (mesh 칼럼 추가됨)
        taxi_df = MapMatching.prep_taxi_data(taxi_file, taxi_col)

        # Perform map matching
        res = map_matcher.do_map_matching(taxi_df, link_df)

        # Save result
        res.to_csv(output_file, index=False)
        print("MapMatching completed!")

    @staticmethod
    def map_matching_func(input_file, output_file):
        # args
        data_input_path = Path(global_var[DATA_INPUT], input_file)
        data_output_path = Path(global_var[DATA_OUTPUT], output_file)
        data_big_input = Path(global_var[DATA_BIG_INPUT], "node_link_data.csv")

        taxi_file = data_input_path
        link_dir = data_big_input
        output_file = data_output_path

        select_col = "vehicle,date,month_created,area_code,x_bessel,y_bessel,status,company_code,driver_ID,x_wgs84,y_wgs84"

        # 파일 인코딩 확인

        # If input arguments are provided, use them
        # taxi_file = sys.argv[1]
        # link_dir = sys.argv[2]
        # output_file = sys.argv[3]
        # select_col = sys.argv[4]

        taxi_col = select_col.split(",")  # 문자열 -> 리스트

        # Load link data
        link_df = pd.read_csv(link_dir, encoding="utf-8")

        # 택시 관련 데이터 전처리 작업 (mesh 칼럼 추가됨)
        taxi_df = MapMatching.prep_taxi_data(taxi_file, taxi_col)

        # Perform map matching
        res = map_matcher.do_map_matching(taxi_df, link_df)

        # Save result
        res.to_csv(output_file, index=False)
        print("MapMatching completed!")

    @staticmethod
    def prep_taxi_data(taxi_dir, taxi_col):
        """Mesh 칼럼 추가'"""
        # Load raw taxi data
        with open(taxi_dir, "rb") as f:
            result = chardet.detect(f.read())
            encoding = result["encoding"]

        print(f"파일 인코딩: {encoding}")

        raw_taxi_df = pd.read_csv(taxi_dir, encoding=encoding)
        print(raw_taxi_df.head())

        # Select relevant columns
        raw_taxi_df = raw_taxi_df[taxi_col]

        # 위도경도 데이터 이용하여 mesh 그리드 값 생성
        raw_taxi_df["mesh"] = raw_taxi_df.apply(
            lambda row: utilsfunc.get_mesh_total(row["x_wgs84"], row["y_wgs84"]),
            axis=1,
        )

        return raw_taxi_df


if __name__ == "__main__":
    MapMatching.main()
