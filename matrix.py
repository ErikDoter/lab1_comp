from pathlib import Path
import numpy as np

class Matrix(object):
    matrix: np.matrix
    sumRows: np.array
    deltaRows: np.array

    def __init__(self, file: Path) -> None:
        self.matrix = np.loadtxt(file)
        self.sumRows = np.array([])
        self.deltaRows = np.array([])

    def print_matrix(self):
        print(f'Матрица:\n {self.matrix}\n\n\n Сумма строк:\n {self.sumRows}\n\n\n\n Непонятная хрень строк:\n {self.deltaRows}')
        

matrix = Matrix()
print(matrix.print_matrix())