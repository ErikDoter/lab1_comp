from typing import List
from matrix import Matrix
from pathlib import Path


class System:
    matrix: Matrix
    result_containers: List[List[int]]

    def __init__(self):
        self.init_values = {
            "test20.txt": [3,3,4,5,5],
            "test50.txt": [10,13,15,17],
            "test101.txt": [3,4,5,7,11],
            "test250.txt": [30,45,55,70,80],
            "test777.txt": [7,17,27,37,47,57,67,77],
            "test1000.txt": [100,125,175,225],
            "test10000.txt": [1000,2000,2500,3000]
        }
        for index in self.init_values:
            self.matrix = Matrix(Path(index))
            self.result_containers = []
            break



    def run(self):
        containers = self.init_values["test20.txt"]
        while not all(self.matrix.is_deleted):
            min_element = self.matrix.min_by_sum()
            delete_cols = self.matrix.get_intesection_row(min_element)
            # первый приоритет
            for i, c in enumerate(containers):
                if c == len(delete_cols):
                    self.result_containers.append(delete_cols)
                    del containers[i]
                    for v in delete_cols:
                        self.matrix.delete_cr(v)




