from matrix import Matrix
from pathlib import Path
from typing import List
import math


class Step2:
    matrix: List[List]
    containers: List[List]
    plata: List[List]
    p_sums: List[int]
    k_arrays: List[List[int]]
    sequence_list: List[int]


    def __init__(self, filename, containers):
        self.init_matrix = Matrix(Path(filename))
        self.init_matrix.print_matrix()
        self.containers = containers
        self.plata = []
        self.p_sums = []
        self.k_arrays = []
        self.sequence_list = []

    def create_containers_matrix(self):
        self.matrix = []
        for index1, container1 in enumerate(self.containers):
            row = []
            for index2, container2 in enumerate(self.containers):
                if index1 != index2:
                    row.append(self.init_matrix.get_container_intersection(container1, container2))
                else:
                    row.append(0)
            self.matrix.append(row)
        for c in self.matrix:
            self.p_sums.append(sum(c))
        print('p_sums = ', self.p_sums)

    def prepare_plata(self):
        dimension = math.ceil(math.sqrt(len(self.containers)))
        for i in range(dimension):
            self.plata.append([])
        for i in range(dimension):
            for j in range(dimension):
                self.plata[i].append(-1)

    def print_matrix(self):
        for i, _ in enumerate(self.matrix):
            print(f'{self.matrix[i]}')

    def rec_k(self, stars: List[int]):
        if len(stars) == len(self.matrix):
            self.sequence_list = stars
            return
        k = []
        for index_row, row in enumerate(self.matrix):
            if index_row in stars:
                k.append("*")
                continue
            double_sum = 0
            for index_col, col in enumerate(self.matrix[index_row]):
                if index_col in stars:
                    double_sum += col
            double_sum *= 2
            k_result = double_sum - self.p_sums[index_row]
            k.append(k_result)
        self.k_arrays.append(k)

        max_k = -10
        for key in k:
            if key != '*' and key > max_k:
                max_k = key
        for i, key in enumerate(k):
            if key == max_k:
                stars.append(i)
        self.rec_k(stars)

    def run(self):
        self.rec_k([0])
        print('_________K_______')
        for a in self.k_arrays:
            print(a)
        print('sequence = ', self.sequence_list)

        flag = True
        for index_row, row in enumerate(self.plata):
            if flag:
                for index_col in range(len(self.plata)):
                    self.plata[index_row][index_col] = self.sequence_list.pop(0)
                flag = False
            else:
                for index_col in reversed(range(len(self.plata))):
                    self.plata[index_row][index_col] = self.sequence_list.pop(0)
                flag = True

        for p in self.plata:
            print(p)


