from pathlib import Path

import pandas as pd
import numpy as np
import time

from etri_gg_py.web.api.gonggan.svdd.utils import SVDDFunction
from etri_gg_py.web.lifespan import DATA_INPUT, DATA_OUTPUT, global_var


def main(args):
    input_file = args[0] #입력 파일 경로
    output_file = args[1] #출력할 파일 경로
    hour = int(args[2]) # 0 분석하고자 하는 시간대
    c_value = float(args[3]) # 0.1 종속 변수 명
    selected_col = str(args[4]) #  "Date,Hour,Code,ma0,ma10,ma20,ma30,ma40,ma50,ma60+,fa0,fa10,fa20,fa30,fa40,fa50,fa60+"

    svdd_exec(input_file, output_file, hour, c_value, selected_col)


def do_svdd(input_file, output_file, hour, c_value):
    svdd_exec(input_file, output_file, hour, c_value, "")


def svdd_exec(data_input_path, data_output_path, hour, c_value, selected_col):
    input_file = Path(global_var[DATA_INPUT], data_input_path)
    output_file = Path(global_var[DATA_OUTPUT], data_output_path)

    if len(selected_col.split(",")) < 2:
        selected_col = "Date,Hour,Code,ma0,ma10,ma20,ma30,ma40,ma50,ma60+,fa0,fa10,fa20,fa30,fa40,fa50,fa60+"
    print(f"{selected_col} selected")

    matrix_calc = SVDDFunction()

    #SVDD parameters
    ABSTOL = 1e-7
    FEASTOL = 1e-7
    RELTOL = 1e-6
    MAXITERS = 100
    STEP = 0.99
    EXPON = 3


    raw_df = pd.read_csv(input_file)
    selected_df = raw_df[selected_col.split(",")]

    """----------------------------------------------minmax 스케일링으로 정규화------------------------------------------------------------------------"""
    # 최대 최소 값 추출 (GroupBy)
    minmax_df = selected_df.groupby(['Code', 'Hour']).agg(
        max_ma0=('ma0', 'max'),
        min_ma0=('ma0', 'min'),
        max_ma10=('ma10', 'max'),
        min_ma10=('ma10', 'min'),
        max_ma20=('ma20', 'max'),
        min_ma20=('ma20', 'min'),
        max_ma30=('ma30', 'max'),
        min_ma30=('ma30', 'min'),
        max_ma40=('ma40', 'max'),
        min_ma40=('ma40', 'min'),
        max_ma50=('ma50', 'max'),
        min_ma50=('ma50', 'min'),
        max_ma60_plus=('ma60+', 'max'),
        min_ma60_plus=('ma60+', 'min'),
        max_fa0=('fa0', 'max'),
        min_fa0=('fa0', 'min'),
        max_fa10=('fa10', 'max'),
        min_fa10=('fa10', 'min'),
        max_fa20=('fa20', 'max'),
        min_fa20=('fa20', 'min'),
        max_fa30=('fa30', 'max'),
        min_fa30=('fa30', 'min'),
        max_fa40=('fa40', 'max'),
        min_fa40=('fa40', 'min'),
        max_fa50=('fa50', 'max'),
        min_fa50=('fa50', 'min'),
        max_fa60_plus=('fa60+', 'max'),
        min_fa60_plus=('fa60+', 'min')
    ).reset_index()

    # 조인 (merge)
    joined_df = selected_df.merge(
        minmax_df,
        left_on=['Code', 'Hour'],
        right_on=['Code', 'Hour'],
        how='left'
    )

    # 정규화
    joined_df['norm_ma0'] = (joined_df['ma0'] - joined_df['min_ma0']) / (joined_df['max_ma0'] - joined_df['min_ma0'])
    joined_df['norm_ma10'] = (joined_df['ma10'] - joined_df['min_ma10']) / (
                joined_df['max_ma10'] - joined_df['min_ma10'])
    joined_df['norm_ma20'] = (joined_df['ma20'] - joined_df['min_ma20']) / (
                joined_df['max_ma20'] - joined_df['min_ma20'])
    joined_df['norm_ma30'] = (joined_df['ma30'] - joined_df['min_ma30']) / (
                joined_df['max_ma30'] - joined_df['min_ma30'])
    joined_df['norm_ma40'] = (joined_df['ma40'] - joined_df['min_ma40']) / (
                joined_df['max_ma40'] - joined_df['min_ma40'])
    joined_df['norm_ma50'] = (joined_df['ma50'] - joined_df['min_ma50']) / (
                joined_df['max_ma50'] - joined_df['min_ma50'])
    joined_df['norm_ma60_plus'] = (joined_df['ma60+'] - joined_df['min_ma60_plus']) / (
                joined_df['max_ma60_plus'] - joined_df['min_ma60_plus'])
    joined_df['norm_fa0'] = (joined_df['fa0'] - joined_df['min_fa0']) / (joined_df['max_fa0'] - joined_df['min_fa0'])
    joined_df['norm_fa10'] = (joined_df['fa10'] - joined_df['min_fa10']) / (
                joined_df['max_fa10'] - joined_df['min_fa10'])
    joined_df['norm_fa20'] = (joined_df['fa20'] - joined_df['min_fa20']) / (
                joined_df['max_fa20'] - joined_df['min_fa20'])
    joined_df['norm_fa30'] = (joined_df['fa30'] - joined_df['min_fa30']) / (
                joined_df['max_fa30'] - joined_df['min_fa30'])
    joined_df['norm_fa40'] = (joined_df['fa40'] - joined_df['min_fa40']) / (
                joined_df['max_fa40'] - joined_df['min_fa40'])
    joined_df['norm_fa50'] = (joined_df['fa50'] - joined_df['min_fa50']) / (
                joined_df['max_fa50'] - joined_df['min_fa50'])
    joined_df['norm_fa60_plus'] = (joined_df['fa60+'] - joined_df['min_fa60_plus']) / (
                joined_df['max_fa60_plus'] - joined_df['min_fa60_plus'])

    # 선택한 열만 추출 후 정렬
    normal_df = joined_df[['Date', 'Code', 'Hour', 'norm_ma0', 'norm_ma10', 'norm_ma20',
                           'norm_ma30', 'norm_ma40', 'norm_ma50', 'norm_ma60_plus',
                           'norm_fa0', 'norm_fa10', 'norm_fa20', 'norm_fa30',
                           'norm_fa40', 'norm_fa50', 'norm_fa60_plus']].sort_values(by='Date')


    """----------------------------------------------minmax 스케일링 완료------------------------------------------------------------------------"""


    """----------------------------------------------SVDD 알고리즘 시작------------------------------------------------------------------------"""

    final_df = pd.DataFrame()

    code_list = raw_df['Code'].drop_duplicates().astype(int).sort_values().values
    # TODO 테스트로 5개만
    # for e in code_list[:5]:
    for e in code_list:
        print(e)
        time.sleep(1)

        #필터링
        # value_selected = normal_df.query("Code == @e and Hour == @hour")
        value_selected = normal_df[(normal_df['Code'] == int(e)) & (normal_df['Hour'] == int(hour))].copy()

        value_size = value_selected.shape[0]

        # 인덱스 추가
        value_selected.loc[:,'dateIndex'] = range(len(value_selected))

        # 이름 바꾼 새로운 DataFrame 생성
        vector_indexed = value_selected.rename(columns={
            "Date": "vecDate",
            "Code": "vecCode",
            "Hour": "vecHour",
            "norm_ma0": "norm_ma0_2",
            "norm_ma10": "norm_ma10_2",
            "norm_ma20": "norm_ma20_2",
            "norm_ma30": "norm_ma30_2",
            "norm_ma40": "norm_ma40_2",
            "norm_ma50": "norm_ma50_2",
            "norm_ma60_plus": "norm_ma60_plus_2",
            "norm_fa0": "norm_fa0_2",
            "norm_fa10": "norm_fa10_2",
            "norm_fa20": "norm_fa20_2",
            "norm_fa30": "norm_fa30_2",
            "norm_fa40": "norm_fa40_2",
            "norm_fa50": "norm_fa50_2",
            "norm_fa60_plus": "norm_fa60_plus_2",
            "dateIndex": "vecIndex"
        })

        # 두 vector_indexed value_selectedㄹ를 'Code' 열을 기준으로 outer join
        vector_joined = pd.merge(value_selected, vector_indexed, left_on='Code', right_on='vecCode', how='outer')

        # 필요한 열 선택
        vector_joined = vector_joined[[
            "Date", "Code", "Hour",
            "norm_ma0", "norm_ma10", "norm_ma20", "norm_ma30", "norm_ma40", "norm_ma50", "norm_ma60_plus",
            "norm_fa0", "norm_fa10", "norm_fa20", "norm_fa30", "norm_fa40", "norm_fa50", "norm_fa60_plus",
            "norm_ma0_2", "norm_ma10_2", "norm_ma20_2", "norm_ma30_2", "norm_ma40_2", "norm_ma50_2", "norm_ma60_plus_2",
            "norm_fa0_2", "norm_fa10_2", "norm_fa20_2", "norm_fa30_2", "norm_fa40_2", "norm_fa50_2", "norm_fa60_plus_2",
            "dateIndex", "vecIndex"
        ]]

        # # dotProduct 열 계산 (내적)후 vector_joined에 추가
        vector_joined['dotProduct'] = (
                vector_joined["norm_ma0"] * vector_joined["norm_ma0_2"] +
                vector_joined["norm_ma10"] * vector_joined["norm_ma10_2"] +
                vector_joined["norm_ma20"] * vector_joined["norm_ma20_2"] +
                vector_joined["norm_ma30"] * vector_joined["norm_ma30_2"] +
                vector_joined["norm_ma40"] * vector_joined["norm_ma40_2"] +
                vector_joined["norm_ma50"] * vector_joined["norm_ma50_2"] +
                vector_joined["norm_ma60_plus"] * vector_joined["norm_ma60_plus_2"] +
                vector_joined["norm_fa0"] * vector_joined["norm_fa0_2"] +
                vector_joined["norm_fa10"] * vector_joined["norm_fa10_2"] +
                vector_joined["norm_fa20"] * vector_joined["norm_fa20_2"] +
                vector_joined["norm_fa30"] * vector_joined["norm_fa30_2"] +
                vector_joined["norm_fa40"] * vector_joined["norm_fa40_2"] +
                vector_joined["norm_fa50"] * vector_joined["norm_fa50_2"] +
                vector_joined["norm_fa60_plus"] * vector_joined["norm_fa60_plus_2"]
        ).astype('float64')

        # 필요한 데이터만 추출하고 kernel_array 생성
        kernel_array = vector_joined[['dotProduct','dateIndex','vecIndex']].to_numpy()


        # norm_data를 2D 배열로 복사
        norm_data = value_selected[['norm_ma0', 'norm_ma10', 'norm_ma20', 'norm_ma30',
                                   'norm_ma40', 'norm_ma50', 'norm_ma60_plus',
                                   'norm_fa0', 'norm_fa10', 'norm_fa20',
                                   'norm_fa30', 'norm_fa40', 'norm_fa50', 'norm_fa60_plus']].to_numpy(dtype=float)

        # 2D 배열에 커널 복사
        H_matrix = np.zeros((value_size, value_size))
        for i in range(value_size * value_size):
            H_matrix[int(kernel_array[i][1]), int(kernel_array[i][2])] = float(kernel_array[i][0])

        # q_matrix 설정
        q_matrix = np.zeros((value_size, 1))
        for i in range(value_size):
            q_matrix[i, 0] = H_matrix[i, i] * 0.5

        # A_matrix 설정
        A_matrix = np.ones((value_size, 1))

        # b_matrix 설정
        b_matrix = np.array([[1.0]])

        # G_matrix 설정
        G_matrix = np.zeros((value_size * 2, value_size))
        for i in range(value_size):
            G_matrix[i, i] = 1.0
            G_matrix[i + value_size, i] = -1.0

        # h_matrix 설정
        h_matrix = np.zeros((value_size * 2, 1))
        for i in range(value_size):
            h_matrix[i, 0] = c_value
            h_matrix[i + value_size, 0] = 0.0

        # 추가 계산
        resx0 = np.sqrt(np.sum(q_matrix ** 2))
        resy0 = b_matrix[0, 0]
        resz0 = np.sqrt(np.sum(h_matrix ** 2))

        # 내적 연산
        IP_G = G_matrix.T @ G_matrix


        # Cholesky 분해

        F_S_matrix = matrix_calc.cholesky(H_matrix + IP_G)

        # 역삼각 행렬 계산
        inv_matrix = matrix_calc.inverse(F_S_matrix)

        # Asct 계산
        Asct = inv_matrix @ A_matrix
        F_K = np.array([[np.sqrt(np.sum(Asct ** 2))]])

        # -------------------------------------------------------------------------------------------

        # 초기화 및 계산
        x = matrix_calc.multiple(inv_matrix,matrix_calc.element_calc(q_matrix, h_matrix, "+"))

        y = np.zeros((1, 1))
        y[0][0] = (matrix_calc.multi_sum(Asct, x) - 1) / matrix_calc.multi_sum(Asct, Asct)

        x = matrix_calc.gemv(Asct, y, x, -1, 1)
        x = matrix_calc.multiple(inv_matrix, x, "T")

        z = matrix_calc.gemv(G_matrix, x, h_matrix, beta = -1)
        s = matrix_calc.scal(-1,z)

        nrmz = np.sqrt(matrix_calc.multi_sum(z, z))
        nrms = np.sqrt(matrix_calc.multi_sum(s, s))


        z = matrix_calc.plus((-1 * matrix_calc.min(z)) + 1, z)
        s = matrix_calc.plus((-1 * matrix_calc.min(s)) + 1, s)


        # 결과 계산용 배열 초기화
        rx = matrix_calc.scal(-1, q_matrix)
        ry = matrix_calc.copy(b_matrix)
        rz = matrix_calc.scal(0, h_matrix)


        dx = matrix_calc.copy(x)
        dy = matrix_calc.copy(y)


        dz = matrix_calc.scal(0,h_matrix)
        ds = matrix_calc.scal(0,h_matrix)

        ws3 = matrix_calc.scal(0.0, np.zeros((value_size * 2, 1), dtype=float))
        wz3 = matrix_calc.scal(0.0, np.zeros((value_size * 2, 1), dtype=float))


        W_d_matrix = 1 + matrix_calc.scal(0, h_matrix)
        W_di_matrix = matrix_calc.copy(W_d_matrix)


        lmbda = matrix_calc.scal(0,h_matrix)
        lmbdasq = matrix_calc.scal(0,h_matrix)


        ts = 0.0
        tz = 0.0
        step = 0.0
        gap = matrix_calc.multi_sum(z, s)

        # 반복 결과를 저장할 데이터 프레임 초기화

        """ ---------------------------------- for loop start  ----------------------------------------- """
        for iters in range(MAXITERS):
            # resx 계산
            rx = -q_matrix.copy()
            rx += H_matrix @ x
            f0 = (np.sum(x * rx) + np.sum(x * -q_matrix)) / 2
            rx += A_matrix @ y
            rx += G_matrix.T @ z #matrixCalc.elementCalc(matrixCalc.multiple(G_matrix, z, "T"), rx,"+")
            resx = np.sqrt(np.sum(rx ** 2))


            # resy 계산
            ry = matrix_calc.copy(b_matrix)
            ry -= A_matrix.T @ x
            resy = np.zeros((1, 1))
            resy[0, 0] = np.sqrt(matrix_calc.multi_sum(ry, ry))



            # resz 계산
            rz = matrix_calc.copy(s)
            rz = matrix_calc.element_calc(s, h_matrix,"-")
            rz = matrix_calc.element_calc(matrix_calc.multiple(G_matrix, x),rz,"+")
            resz = np.sqrt(matrix_calc.multi_sum(rz, rz))

            # 결과 평가
            pcost = f0
            dcost = f0 + matrix_calc.multi_sum(y, resy) + matrix_calc.multi_sum(z,rz) - gap

            if pcost < 0.0:
                relgap = gap / -pcost
            elif dcost == 0.0:
                relgap = gap / dcost
            else:
                relgap = 0.0

            # pres = max(resy/resy0, resz/resz0)
            # dres = resx / resx0
            pres = max(resy[0][0] / resy0, resz / resz0)
            dres = resx / resx0

            # 최적해 발견 조건 확인
            if pres <= FEASTOL and dres <= FEASTOL and (gap <= ABSTOL or (relgap != 0.0 and relgap <= RELTOL)) or iters == MAXITERS:
                ts = -np.min(s)
                tz = -np.min(z)
                if iters == MAXITERS:
                    print("Terminated (maximum number of iterations reached).")
                else:
                    print("Optimal solution found.")

                    # x 값 소수점 자리수 조정
                    x = np.round(x * 10000) / 10000.0

                    # R_3 계산
                    R_3 = 0.0
                    for i in range(value_size):
                        for j in range(value_size):
                            R_3 += np.round(x[i, 0] * 10000) / 10000.0 * np.round(x[j, 0] * 10000) / 10000.0 * np.sum(
                                norm_data[i] * norm_data[j])

                    # Radius 계산
                    radius = np.zeros((value_size, 1))
                    for i in range(value_size):
                        radius[i, 0] = matrix_calc.calc_radius(norm_data[i], norm_data, x, R_3)  # calc_radius 함수 필요

                    # 결과를 result1 데이터프레임으로 변환
                    result1 = np.zeros((value_size, 4))
                    for i in range(value_size):
                        result1[i, 0] = i
                        result1[i, 1] = x[i, 0]
                        result1[i, 2] = radius[i, 0]
                        result1[i, 3] = c_value  # c_value는 설정된 상수

                    result1_df = pd.DataFrame(result1, columns=["Index", "X", "Radius", "c_value"])

                    # vectorIndexed와의 조인
                    result_df = pd.merge(vector_indexed, result1_df, left_on="vecIndex", right_on="Index", how="left")
                    result_df = result_df.sort_values(by="vecDate")

                    # TODO 결과를 각각의 파일로 저장할 떄
                    # result_df.to_csv(f"{output_file}_{int(time.time())}.csv", index=False)

                    # 전체 파일로 저장하기 위해 final_df에 추가
                    final_df = pd.concat([final_df, result_df], ignore_index=True)

                    break  # 반복 종료

            if iters == 0:
                    # W_d_matrix, W_di_matrix 및 lmbda 초기화
                W_d_matrix = np.sqrt(s / z)  # s와 z는 요소별 나눗셈을 수행
                W_di_matrix = np.sqrt(z / s)
                lmbda = np.sqrt(z * s)

            # lmbdasq 계산
            lmbdasq = lmbda ** 2

            # --------------------------------------------  f3 = kktsolver(W) ----------------------------------------------------------
            # F_Gs_matrix 초기화 및 설정
            F_Gs_matrix = np.zeros((value_size * 2, value_size))
            for i in range(value_size):
                F_Gs_matrix[i, i] = W_di_matrix[i, 0]
                F_Gs_matrix[i + value_size, i] = -W_di_matrix[i + value_size, 0]

            # IP_Gs (내적 행렬) 계산
            IP_Gs = F_Gs_matrix.T @ F_Gs_matrix

            # H_matrix와 IP_Gs의 합산 및 Cholesky 분해 적용
            F_S_1_matrix = matrix_calc.cholesky(matrix_calc.element_calc(H_matrix, IP_Gs,"+"))


            # 삼각 행렬의 역행렬 계산
            inv_1_matrix = matrix_calc.inverse(F_S_1_matrix)

            # Asct_1과 F_K_1 계산
            Asct_1 = matrix_calc.multiple(inv_1_matrix, A_matrix)
            F_K_1 = np.sqrt(np.sum(Asct_1 ** 2))  # 모든 요소의 합을 통해 계산

            # --------------------------------------------f3 = kktsolver(W) end---------------------------------------------------------

            # mu, sigma, eta 초기화
            mu = gap / (value_size * 2)
            sigma = 0.0
            eta = 0.0

            for i in range(2):
                # Solve를 위한 행렬 설정
                ds = matrix_calc.scal(0.0, ds)
                if i == 1:
                    ds = matrix_calc.element_calc(matrix_calc.scal(-1, ws3), ds, "+")
                    # ds = -ws3 + ds  # ds와 ws3를 요소별로 더합니다.

                ds = matrix_calc.plus(sigma * mu, matrix_calc.element_calc(matrix_calc.scal(-1, lmbdasq), ds, "+"))
                dx = matrix_calc.scal(-1 + eta, rx)
                dy = matrix_calc.scal(-1 + eta, ry)
                dz = matrix_calc.scal(-1 + eta, rz)

                # --------------------------------f4_no_ir------------------------------------------

                ds = matrix_calc.multiple(matrix_calc.inverse(matrix_calc.diag(lmbda)), ds, "N")
                ws3 = matrix_calc.element_calc(W_d_matrix, ds, "*")
                dz = matrix_calc.element_calc(matrix_calc.scal(-1, ws3), dz, sign="+")

                # --------------------------------f3 solve------------------------------------------

                dz = matrix_calc.multiple(matrix_calc.inverse(matrix_calc.diag(W_d_matrix)), dz, "N")
                dx += F_Gs_matrix.T @ dz  #dx = matrix_calc.element_calc(matrix_calc.multiple(F_Gs_matrix, dz,"T"), dx,"+")  # dx에 dz를 곱하고 F_Gs_matrix를 더합니다.
                dx = matrix_calc.multiple(inv_1_matrix, dx)
                dy[0, 0] = (matrix_calc.multi_sum(Asct_1, dx) - dy[0, 0]) / matrix_calc.multi_sum(Asct_1, Asct_1)
                dx = matrix_calc.gemv(Asct_1, dy, dx, -1, 1)
                dx = matrix_calc.multiple(inv_1_matrix, dx, "T")
                dz = matrix_calc.gemv(F_Gs_matrix, dx, dz, beta = -1)
                # -------------------------------f3 solve end----------------------------------------

                ds = matrix_calc.element_calc(matrix_calc.scal(-1, dz), ds, "+")
                # --------------------------------f4_no_ir end----------------------------------------



                dsdz = matrix_calc.multi_sum(ds, dz)

                if i == 0:
                    # ws3 = ds * dz  # 요소별 곱
                    ws3 = ds
                    ws3 = matrix_calc.element_calc(ws3, dz, "*")

                ds = matrix_calc.multiple(matrix_calc.inverse(matrix_calc.diag(lmbda)), ds, "N")
                dz = matrix_calc.multiple(matrix_calc.inverse(matrix_calc.diag(lmbda)), dz, "N")

                ts = (-1) * matrix_calc.min(ds)
                tz = (-1) * matrix_calc.min(dz)
                t = max(0.0, max(ts, tz))

                if t == 0.0:
                    step = 1.0
                else:
                    if i == 0:
                        step = min(1.0, 1.0 / t)
                    else:
                        step = min(1.0, STEP / t)

                if i == 0:
                    sigma = np.power(min(1.0, max(0.0, 1.0 - step + dsdz / gap * step ** 2)), EXPON)
                    eta = 0.0

            x = matrix_calc.element_calc(matrix_calc.scal(step, dx), x, "+")
            y = matrix_calc.element_calc(matrix_calc.scal(step, dy), y, "+")

            # Update ds and dz with the scaling factor
            ds = matrix_calc.plus(1.0, matrix_calc.scal(step, ds))
            dz = matrix_calc.plus(1.0, matrix_calc.scal(step, dz))

            # Multiply ds and dz by the diagonal of lmbda
            ds = matrix_calc.multiple(matrix_calc.diag(lmbda), ds, "N")
            dz = matrix_calc.multiple(matrix_calc.diag(lmbda), dz, "N")

            # Update lmbda and scaling
            ds = matrix_calc.sqrt(ds)
            dz = matrix_calc.sqrt(dz)
            W_d_matrix = matrix_calc.element_calc(ds, W_d_matrix, "*")
            W_d_matrix = matrix_calc.multiple(matrix_calc.inverse(matrix_calc.diag(dz)), W_d_matrix)
            W_di_matrix = matrix_calc.element_calc(matrix_calc.plus(1.0, matrix_calc.scal(0, W_di_matrix)), W_d_matrix, "/")
            lmbda = matrix_calc.element_calc(ds, dz, "*")



            # Unscale s and z
            s = matrix_calc.copy(lmbda)
            s = matrix_calc.element_calc(W_d_matrix, s, "*")
            z = matrix_calc.copy(lmbda)
            z = matrix_calc.multiple(matrix_calc.inverse(matrix_calc.diag(W_d_matrix)), z)

            # Compute the gap
            gap = matrix_calc.multi_sum(lmbda, lmbda)

    final_df.to_csv(f"{output_file}", index=False)
    print("Done")





if __name__ == "__main__":
    args = ["/home/tiep/dev/gonggan/data/05_02_SVDD/05_02_01_SVDD_input.csv",
            "SVDD_output_kmj.csv",
            "0",
            "0.1",
            "Date,Hour,Code,ma0,ma10,ma20,ma30,ma40,ma50,ma60+,fa0,fa10,fa20,fa30,fa40,fa50,fa60+"]
    main(args)

