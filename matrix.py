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

    def get_intersection_rows(self):
        return []

    def print_matrix(self):
        print(f'Матрица:\n {self.matrix}\n\n\n Сумма строк:\n {self.sumRows}\n\n\n\n Непонятная хрень строк:\n {self.deltaRows}')



        

matrix = Matrix('test50.txt')
