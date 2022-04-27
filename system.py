from typing import List
from matrix import Matrix
from pathlib import Path
import numpy as np
from utils import recursion
from copy import copy


class System:
    matrix: Matrix
    result_containers: List[List[int]]

    def __init__(self):
        self.init_values = {
            "test20.txt": [3,4,5,7],
            "test50.txt": [10,13,15,17],
            "test101.txt": [3,4,5,7,11],
            "test250.txt": [45,55,70,80],
            "test777.txt": [7,17,27,37,47,57,67,77],
            "test1000.txt": [100,100,100,125,175,175,225],
            "test10000.txt": [2000, 2500, 2500, 3000]
        }
        for index in self.init_values:
            self.matrix = Matrix(Path('test20.txt'))
            self.result_containers = []
            break



    def run(self):
        containers = self.init_values["test20.txt"]
        print(containers)
        containers = recursion(20, copy(containers))
        containers.sort()
        print(containers)
        while not all(self.matrix.is_deleted):
            min_element = self.matrix.min_by_sum()
            delete_cols = self.matrix.get_intesection_row(min_element)
            is_found = False
            # первый приоритет
            for i, c in enumerate(containers):
                if c == len(delete_cols):
                    self.result_containers.append(delete_cols)
                    del containers[i]
                    for v in delete_cols:
                        self.matrix.delete_cr(v)
                    is_found = True
                    break
            # Второй приоритет
            if not is_found:
                result = -1
                result_index = -1
                mini = 10000
                for i, c in enumerate(containers):
                    if len(delete_cols) - c < mini and len(delete_cols) - c > 0:
                        mini = len(delete_cols) - c
                        result = c
                        result_index = i
                if result != -1:
                    while result != len(delete_cols):
                        useless = self.matrix.get_max_delta(delete_cols)
                        #delete_cols.remove(useless)
                        delete_cols = np.delete(delete_cols, np.argwhere(delete_cols == useless))
                    self.result_containers.append(delete_cols)
                    del containers[result_index]
                    for v in delete_cols:
                        self.matrix.delete_cr(v)
                    is_found = True
            if not is_found:
                c = containers[0]
                count = c - len(delete_cols)
                missing = self.matrix.get_intersection_rows_rows(delete_cols, count)
                for m in missing:
                    delete_cols = np.append(delete_cols, m)
                self.result_containers.append(delete_cols)
                del containers[0]
                for v in delete_cols:
                    self.matrix.delete_cr(v)
        print(self.result_containers)







