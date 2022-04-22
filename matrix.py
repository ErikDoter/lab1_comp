from pathlib import Path
from re import S
import numpy as np
from typing import List

class Matrix(object):
    matrix: np.matrix
    sumRows: np.array
    deltaRows: np.array
    is_deleted: List[bool]

    def __init__(self, file: Path) -> None:
        self.matrix = np.loadtxt(file, delimiter=', ')
        self.sumRows = np.sum(self.matrix,axis=1).tolist()
        self.deltaRows = np.array([])
        self.is_deleted = []
        for i in range(len(self.sumRows)):
            self.is_deleted.append(False)

    def delete_cr(self, cr):
        for i, _ in enumerate(self.matrix):
            for j, _ in enumerate(self.matrix[i]):
                if i == cr or j == cr:
                    self.matrix[i][j] = 0
        self.sumRows = np.sum(self.matrix, axis=1).tolist()
        self.is_deleted[int(cr)] = True

    def get_deltas(self, arr: np.array) -> dict:
        res = {}
        for i in arr:
            dec = 0 #сумма в выделенных стобцах
            for j in arr:
                dec = dec + self.matrix[i][j]
            res[i] = self.sumRows - dec
        return res

    def get_max_delta(self, arr: np.array) -> int:
        maxd = -1
        res = 0
        for i in arr:
            dec = 0  # сумма в выделенных стобцах
            for j in arr:
                dec = dec + self.matrix[i][j]
            delta = self.sumRows[i] - dec
            if maxd < delta:
                maxd = delta
                res = i
        return res

    def min_by_sum(self) -> int:
        mins = 100000
        res = -1
        for i, v in enumerate(self.sumRows):
            if v < mins and v != 0:
                mins = v
                res = i
        return res

    def get_intesection_row(self, row: int) -> np.array:
        res = np.array([row])
        for i, _ in enumerate(self.matrix[row]):
            if self.matrix[row][i] != 0:
                res = np.append(res, i)
        
        return res

    def get_intersection_rows_rows(self, rows: np.array, count: int) -> np.array:
        res = []
        for i in rows:
            res = np.append(res, self.get_intesection_row(i))
        res = np.unique(res)
        for r in rows:
            res = np.delete(res, np.argwhere(res == r))
        if len(res) < count:
            res = np.append(res, self.get_intersection_rows_rows(np.append(rows,res).astype(int), count - len(res)))
        elif len(res) > count:
            res = res[:count]
        return res



    def print_matrix(self):
        print(f'Матрица:\n {self.matrix}\n\n\n Сумма строк:\n {self.sumRows}\n\n\n\n Непонятная хрень строк:\n {self.deltaRows}')


