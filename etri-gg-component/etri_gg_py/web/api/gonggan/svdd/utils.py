import numpy as np


class SVDDFunction:
    def __init__(self):
        pass

    # Radius Calculation
    def calc_radius(self,array1, array2, array3, r_3):
        r_1 = np.dot(array1, array1)  # arr_multi_sum(array1, array1)과 동일

        # R_2 계산
        r_2 = sum(array3[i][0] * np.dot(array1, array2[i]) for i in range(len(array2)))

        # 결과 계산
        result = np.sqrt(r_1 - 2 * r_2 + r_3)

        return result

    # Single Dimension Array Inner Product
    def arr_multi_sum(self, array1, array2):
        size = len(array1)
        result = 0.0

        for i in range(size):
              result += float(array1[i]) * float(array2[i])

        return result
        # return sum(a * b for a, b in zip(array1, array2))

    # 2D 배열에서 대각행렬 생성
    def diag(self, array):
        return np.diag([row[0] for row in array])

    # Square root of each element
    def sqrt(self, array):
        return np.sqrt(array)

    # Copy a 2D array
    def copy(self, array):
        return np.copy(array)

    # Minimum value in a 2D array
    def min(self, array):
        return np.min(array)

    # 2D 베열 덧셈
    def plus(self, x, array):
        return array + x

    # Scale each element by x
    def scal(self, x, array):
        return x * array

    # General matrix-vector multiplication
    def gemv(self, Array1, Array2, Array3, alpha=1.0, beta=0.0):
        row_size = Array1.shape[0]
        col_size = Array1.shape[1]

        result = np.zeros((row_size, 1))
        for i in range(row_size):
            if Array2.shape[0] == 1:
                result[i, 0] = (Array1[i, 0] * Array2[0, 0] * alpha) + (Array3[i, 0] * beta)
            else:
                temp_sum = 0.0
                for j in range(col_size):
                    temp_sum += (Array1[i, j] * Array2[j, 0] * alpha)
                result[i, 0] = temp_sum + (Array3[i, 0] * beta)

        return result

    # Sum of products of corresponding elements in two single-column 2D arrays
    def multi_sum(self, array1, array2):

        # temp_sum = 0.0
        # # 배열의 행 크기 확인
        # row_size = array1.shape[0]
        # # 요소별 곱의 합 계산
        # for i in range(row_size):
        #     temp_sum += array1[i][0] * array2[i][0]
        # return temp_sum
        return np.sum(array1[:, 0] * array2[:, 0])

    # Inner product of a matrix with its transpose
    def inner_product(self, array1):
        return np.dot(array1.T, array1)

    # Matrix multiplication with optional transpose of the first matrix
    def multiple(self, array1, array2, trans="N"):
        # 배열 크기 확인
        if array1.shape[1] != array2.shape[0]:
            raise ValueError("Check array size")

        row_size = array1.shape[0]
        row_size2 = array2.shape[0]
        col_size2 = array2.shape[1]

        multi_matrix = np.zeros((row_size, col_size2))

        # 전치 옵션에 따른 반복 크기 설정
        if trans == "N":
            iter_size = row_size
        elif trans == "T":
            iter_size = array1.shape[1]

        # 행렬 곱셈 수행
        for i in range(iter_size):
            for j in range(col_size2):
                multi_sum = 0.0
                if trans == "N":
                    for k in range(row_size2):
                        multi_sum += array1[i][k] * array2[k][j]
                elif trans == "T":
                    for k in range(row_size):
                        multi_sum += array1[k][i] * array2[k][j]
                multi_matrix[i][j] = multi_sum

        return multi_matrix

    def element_calc(self, array1, array2, sign):
        row_size = min(len(array1), len(array2))
        col_size = min(len(array1[0]), len(array2[0]))

        sum_matrix = np.zeros((row_size, col_size))

        if sign == "+":
            for i in range(row_size):
                for j in range(col_size):
                    sum_matrix[i][j] = array1[i][j] + array2[i][j]

        elif sign == "-":
            for i in range(row_size):
                for j in range(col_size):
                    sum_matrix[i][j] = array1[i][j] - array2[i][j]

        elif sign == "*":
            for i in range(row_size):
                for j in range(col_size):
                    sum_matrix[i][j] = array1[i][j] * array2[i][j]

        elif sign == "/":
            for i in range(row_size):
                for j in range(col_size):
                    sum_matrix[i][j] = array1[i][j] / array2[i][j]

        return sum_matrix

    # Cholesky Decomposition
    def cholesky(self, array1):
        row_size = array1.shape[0]
        chol_matrix = np.zeros_like(array1)

        chol_matrix[0, 0] = np.sqrt(array1[0, 0])

        for i in range(1, row_size):
            chol_matrix[i, 0] = array1[i, 0] / chol_matrix[0, 0]

        for j in range(1, row_size):
            for i in range(row_size):
                if j > i:
                    chol_matrix[i, j] = array1[i, j]
                elif j == i:
                    row_sum = sum(chol_matrix[i, k] ** 2 for k in range(j))
                    chol_matrix[i, j] = np.sqrt(array1[i, j] - row_sum)
                else:
                    row_sum = sum(chol_matrix[i, k] * chol_matrix[j, k] for k in range(j))
                    chol_matrix[i, j] = (array1[i, j] - row_sum) / chol_matrix[j, j]

        return chol_matrix

    # Inverse of a matrix
    def inverse(self, array1):
        row_size = array1.shape[0]
        col_size = array1.shape[1]

        inverse_lower = np.zeros((row_size, col_size))
        array1_matrix = np.copy(array1)  # 입력 배열의 복사본

        # 행렬 초기화
        for i in range(row_size):
            for j in range(col_size):
                if i < j:
                    array1_matrix[i, j] = 0.0
                else:
                    array1_matrix[i, j] = array1[i, j] / array1[i, i]

        # 주대각선 위치 설정
        for i in range(row_size):
            inverse_lower[i, i] = 1.0

        # 첫 번째 상대 위치 설정
        for i in range(1, row_size):
            inverse_lower[i, i - 1] = -array1_matrix[i, i - 1]

        # 두 번째 상대 위치부터 계산
        for i in range(2, row_size):
            for j in range(row_size - i):
                calc_sum = 0.0
                for k in range(col_size):
                    calc_sum += inverse_lower[i + j, k] * array1_matrix[k, j] * -1
                inverse_lower[i + j, j] = calc_sum

        # 주대각선 위치 조정
        for i in range(row_size):
            for j in range(col_size):
                if i >= j:
                    inverse_lower[i, j] /= array1[j, j]

        inverse_matrix = self.inner_product(inverse_lower)

        return inverse_lower
