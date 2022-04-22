from pathlib import Path
from re import S
import numpy as np

class Matrix(object):
    matrix: np.matrix
    sumRows: np.array
    deltaRows: np.array

    def __init__(self, file: Path) -> None:
        self.matrix = np.loadtxt(file, delimiter=', ')
        self.sumRows = np.sum(self.matrix,axis=1).tolist()
        self.deltaRows = np.array([])

    def delete_cr(self, cr):
        for i, _ in enumerate(self.matrix):
            for j, _ in enumerate(self.matrix[i]):
                if i == cr or j == cr:
                    self.matrix[i][j] = 0
        self.sumRows = np.sum(self.matrix,axis=1).tolist()

    def get_deltas(self, arr: np.array) -> dict:
        res = {}
        for i in arr:
            dec = 0 #сумма в выделенных стобцах
            for j in arr:
                dec = dec + self.matrix[i][j]
            res[i] = self.sumRows - dec
        return res

    def min_by_sum(self) -> int:
        return np.argmin(self.sumRows)

    def get_intesection_row(self, row: int) -> np.array:
        res = np.array([row])
        for i, _ in self.matrix[row]:
            if self.matrix[row][i] != 0:
                res = np.append(res, i)
        
        return res

    def get_intersection_rows_rows(self, rows: np.array, count: int) -> np.array:
        res = []
        for i in rows:
            res = np.append(res, self.get_intesection_row(i))
        res = np.unique(res)
        res = np.delete(res, rows)
        return res



    def print_matrix(self):
        print(f'Матрица:\n {self.matrix}\n\n\n Сумма строк:\n {self.sumRows}\n\n\n\n Непонятная хрень строк:\n {self.deltaRows}')

        

matrix = Matrix('test20.txt')
print(matrix.print_matrix())