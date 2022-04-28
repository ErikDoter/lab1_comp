from copy import copy
from pathlib import Path
import numpy as np
from typing import List

class Matrix(object):
    init_matrix: np.matrix
    matrix: np.matrix
    sumRows: np.array
    deltaRows: np.array
    is_deleted: List[bool]

    def __init__(self, file: Path) -> None:
        self.matrix = np.loadtxt(file, delimiter=', ')
        self.init_matrix = copy(self.matrix)
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
            if len(res) == 0:
                for index, value in enumerate(self.is_deleted):
                    if not value and index not in res and index not in rows and len(res) < count:
                        res = np.append(res, index)
            else:
                res = np.append(res, self.get_intersection_rows_rows(np.append(rows,res).astype(int), count - len(res)))
        elif len(res) > count:
            res = res[:count]
        return res

    def get_q(self, ll):
        q = 0
        for l in ll:
            for el in l:
                q += np.sum(self.init_matrix[int(el)])
                for e in l:
                    q -= self.init_matrix[int(el)][int(e)]
        return q

    def get_container_intersection(self, container1, container2):
        summa = 0
        for i1, c1 in enumerate(container1):
            for i2, c2 in enumerate(container2):
                summa += self.matrix[int(c1)][int(c2)]
        return int(summa)





    def print_matrix(self):
        print(f'Матрица:\n {self.matrix}\n\n\n Сумма строк:\n {self.sumRows}\n\n\n\n Непонятная хрень строк:\n {self.deltaRows}')


