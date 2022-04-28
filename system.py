from mimetypes import init
from typing import List
from matrix import Matrix
from pathlib import Path
import numpy as np
from utils import rec
from copy import copy

FILE = "test20.txt"

class System:
    matrix: Matrix
    result_containers: List[List[List[int]]]

    def __init__(self):
        self.init_values = {
            "test20.txt": [20, [3,4,5,7]],
            "test50.txt": [50, [10,13,15,17]],
            "test250.txt": [250, [45,55,70,80]],
            "test1000.txt": [1000, [100,100,100,125,175,175,225]],
            #"test10000.txt": [2000, 2500, 2500, 3000]
        }
        self.matrix = Matrix(Path(FILE))
        self.result_containers = []



    def run(self):
        total_containers = rec(self.init_values[FILE][0], self.init_values[FILE][1])
        for containers in total_containers:
            print(containers)
            self.matrix = Matrix(Path(FILE))
            res_containers = []
            while not all(self.matrix.is_deleted):
                min_element = self.matrix.min_by_sum()
                delete_cols = self.matrix.get_intesection_row(min_element)
                is_found = False
                # первый приоритет
                for i, c in enumerate(containers):
                    if c == len(delete_cols):
                        res_containers.append(delete_cols.tolist())
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
                        res_containers.append(delete_cols.tolist())
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
                    res_containers.append(delete_cols.tolist())
                    del containers[0]
                    for v in delete_cols:
                        self.matrix.delete_cr(v)
            self.result_containers.append(res_containers)
        for cons in self.result_containers:
            print('container:')
            print(cons)
            res = []
            init_container = copy(cons)
            #print(container_before)
            #count_container = container_before[0]
            #container_before = container_before[1:]
            #print(count_container)
            #print(container_before)
            while len(init_container) > 1:
                max_elem = 1
                while max_elem > 0:
                    #print(max_elem)
                    #print(init_container)
                    count_container = init_container[0]
                    container_before = init_container[1:]
                    count_elem_before = sum(len(row) for row in container_before)
                    #print(container_before)
                    oned_container_before = sum(container_before, [])
                    #print('rofl',oned_container_before)
                    R_matrix = np.zeros((len(count_container), count_elem_before))
                    for row, e_r in enumerate(R_matrix):
                        for col, e_c in enumerate(R_matrix[row]):
                            cont = []
                            for container in container_before:
                                if oned_container_before[col] in container:
                                    cont = container
                            #print(col, cont)
                            #print(count_container[row], cont)
                            #print(count_container[row], oned_container_before[col])
                            #print(f's1_1 - intersection {count_container[row]} and {cont}')
                            #print(f's2_2 - intersection {count_container[row]} and {count_container}')
                            S1_1 = self.matrix.get_intersection_row_container(row=count_container[row], container=cont)
                            S1_2 = self.matrix.get_intersection_row_container(row=count_container[row], container=count_container)
                            S2_1 = self.matrix.get_intersection_row_container(row=oned_container_before[col], container=count_container)
                            S2_2 = self.matrix.get_intersection_row_container(row=oned_container_before[col], container=cont)
                            #print('S1 = ', S1_1, 'S2 = ',  S1_2)
                            S_inter = self.matrix.get_intersection_row_col(row=count_container[row], col=oned_container_before[col])
                            R_matrix[row][col] = (S1_1 - S1_2) + (S2_1 - S2_2) - 2*S_inter
                    #print(R_matrix)
                    max_elem = R_matrix.max()
                    if max_elem > 0:
                        result = np.where(R_matrix == max_elem)
                        list_max = list(zip(result[0], result[1]))[0]
                        #print(list_max)
                        #print(count_container)
                        max1 = int(count_container[list_max[0]])
                        #print(max1)
                        max2 = int(oned_container_before[list_max[1]])
                        #print(max2)
                        i1, j1 = 0, 0
                        i2, j2 = 0, 0
                        #print(init_container)
                        for i, _ in enumerate(init_container):
                            for j, _ in enumerate(init_container[i]):
                                count = int(init_container[i][j])
                                if max1 == count:
                                    i1, j1 = i, j
                                if max2 == count:
                                    i2, j2 = i, j
                        #print(i1,j1)
                        #print(i2,j2)
                        init_container[i1][j1], init_container[i2][j2] = init_container[i2][j2], init_container[i1][j1]
                    #print(init_container)
                res.append(init_container[0])
                init_container = init_container[1:]
            res.append(init_container[0])
            
            print(res)

            #for con in cons:
               #print(con)    


    def get_best_container(self):
        min = 100000
        min_container = []
        for c in self.result_containers:
            q = self.matrix.get_q(c)
            print('q = ', q)
            if q < min:
                min = q
                min_container = copy(c)
        print('min = ', min)
        return min_container








