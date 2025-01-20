from pathlib import Path

import pandas as pd
import chardet

from etri_gg_py.web.api.gonggan.oosp.map_matcher_oops import do_map_matching
from etri_gg_py.web.api.gonggan.oosp.utils import Utils
from etri_gg_py.web.lifespan import DATA_INPUT, DATA_OUTPUT, DATA_BIG_INPUT, global_var

utilsfunc = Utils()

class OopsMain:
    @staticmethod
    def main():
        # args
        taxi_file = "../../data/OOSP/OOSP_input_kmj.csv"   # 이 데이터는 맵매칭 파일을 이용하여 데이터 만듦, 택시 데이터 map matching에 사용한 input이 맞는 데이터임 oosp에 있는 파일은 변수가 다름 스칼라 코드는 둘 다 맵매칭에 있는 파일 사용함 KeyError: "['vehicle', 'month_created', 'x_bessel', 'y_bessel', 'status', 'company_code', 'driver_ID', 'x_wgs84', 'y_wgs84'] not in index"
        link_dir = "../../data/its_transport_information/new_link_data.csv"
        output_file = "../../data/OOSP/OOSP_output_kmj_by_document.csv"
        select_col = "vehicle,date,month_created,area_code,x_bessel,y_bessel,status,company_code,driver_ID,x_wgs84,y_wgs84"

        # 파일 인코딩 확인

        # If input arguments are provided, use them
        # taxi_file = sys.argv[1]
        # link_dir = sys.argv[2]
        # output_file = sys.argv[3]
        # select_col = sys.argv[4]

        taxi_col = select_col.split(",") # 문자열 -> 리스트

        # Load link data
        link_df = pd.read_csv(link_dir, encoding='utf-8')

        #택시 관련 데이터 전처리 작업
        taxi_df = OopsMain.prep_taxi_data(taxi_file,taxi_col)

        # Perform map matching
        res = do_map_matching(taxi_df, link_df)

        # Save result
        res.to_csv(output_file, index=False)
        print("MapMatching completed!")

    @staticmethod
    def do_oosp(input_file, output_file):
        # 이 데이터는 맵매칭 파일을 이용하여 데이터 만듦, 택시 데이터 map matching에 사용한 input이 맞는 데이터임 oosp에 있는 파일은 변수가 다름 스칼라 코드는 둘 다 맵매칭에 있는 파일 사용함 KeyError: "['vehicle', 'month_created', 'x_bessel', 'y_bessel', 'status', 'company_code', 'driver_ID', 'x_wgs84', 'y_wgs84'] not in index"
        taxi_file = Path(global_var[DATA_INPUT], input_file)
        link_dir = Path(global_var[DATA_BIG_INPUT], "node_link_data.csv")
        output_file = Path(global_var[DATA_OUTPUT], output_file)
        select_col = "vehicle,date,month_created,area_code,x_bessel,y_bessel,status,company_code,driver_ID,x_wgs84,y_wgs84"

        # 파일 인코딩 확인

        # If input arguments are provided, use them
        # taxi_file = sys.argv[1]
        # link_dir = sys.argv[2]
        # output_file = sys.argv[3]
        # select_col = sys.argv[4]

        taxi_col = select_col.split(",")  # 문자열 -> 리스트

        # Load link data
        link_df = pd.read_csv(link_dir, encoding='utf-8')

        # 택시 관련 데이터 전처리 작업
        taxi_df = OopsMain.prep_taxi_data(taxi_file, taxi_col)

        # Perform map matching
        res = do_map_matching(taxi_df, link_df)

        # Save result
        res.to_csv(output_file, index=False)
        print("MapMatching completed!")

    @staticmethod
    def prep_taxi_data(taxi_dir,taxi_col):
        """ mesh 칼럼 추가'"""
        # Load raw taxi data
        with open(taxi_dir, 'rb') as f:
            result = chardet.detect(f.read())
            encoding = result['encoding']

        print(f"파일 인코딩: {encoding}")

        raw_taxi_df = pd.read_csv(taxi_dir, encoding=encoding)
        print(raw_taxi_df.head())

        # Select relevant columns
        raw_taxi_df = raw_taxi_df[taxi_col]

        # mesh 칼럼 추가
        raw_taxi_df['mesh'] = raw_taxi_df.apply(lambda row: utilsfunc.get_mesh_total(row['x_wgs84'], row['y_wgs84']), axis=1)

        return raw_taxi_df


if __name__ == "__main__":
    OopsMain.main()
