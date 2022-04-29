from operator import isub
from numpy import mat
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
    lv: List[float]


    def __init__(self, filename, containers):
        self.init_matrix = Matrix(Path(filename))
        self.init_matrix.print_matrix()
        self.containers = containers
        self.plata = []
        self.p_sums = []
        self.k_arrays = []
        self.sequence_list = []
        self.lv = [0] * len(self.containers)

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


    def get_q(self):
        q = 0
        for index_row, row in enumerate(self.matrix):
            for index_col, col in enumerate(self.matrix):
                massa = self.matrix[index_row][index_col]
                x_coord1 = 0
                y_coord1 = 0
                x_coord2 = 0
                y_coord2 = 0
                for index_row2, row2 in enumerate(self.plata):
                    for index_col2, col2 in enumerate(self.plata):
                        if self.plata[index_row2][index_col2] == index_row:
                            x_coord1 = index_col2
                            y_coord1 = index_row2
                for index_row3, row3 in enumerate(self.plata):
                    for index_col3, col3 in enumerate(self.plata):
                        if self.plata[index_row3][index_col3] == index_col:
                            x_coord2 = index_col3
                            y_coord2 = index_row3
                s = math.fabs(x_coord1 - x_coord2) + math.fabs(y_coord1 - y_coord2)
                q += s * massa
        return q/2
    
    def get_index_in_plata(self, elem: int): #координаты на плате
        for i, x in enumerate(self.plata):
            if elem in x:
                return (i, x.index(elem))

    def get_q_elem(self, elem: int): #считает q для элемента
        x, y = self.get_index_in_plata(elem=elem)
        sum_q_for_el = 0
        for i, row in enumerate(self.plata):
            for j, col in enumerate(row): 
                        s = math.fabs(x-j) + math.fabs(y-i)
                        sum_q_for_el += self.matrix[col][elem] * s

        return sum_q_for_el

    def get_q_elem_x(self, elem: int): #считает q для расстояний по x
        x, y = self.get_index_in_plata(elem=elem)
        sum_q_for_el = 0
        for i, row in enumerate(self.plata):
            for j, col in enumerate(row):
                        s = math.fabs(x-j)
                        sum_q_for_el += self.matrix[col][elem] * s

        return sum_q_for_el

    
    def get_q_elem_y(self, elem: int): #считает q для расстояний по y
        x, y = self.get_index_in_plata(elem=elem)
        sum_q_for_el = 0
        for i, row in enumerate(self.plata):
            for j, col in enumerate(row):
                        s = math.fabs(y-i)
                        sum_q_for_el += self.matrix[col][elem] * s

        return sum_q_for_el
        
    
    def count_lv(self): #счтает lv для всез элементов
        for i, row in enumerate(self.plata):
            for j, col in enumerate(row):
                self.lv[col] = (1/self.p_sums[col]) * self.get_q_elem(col)
        print('lv:', self.lv)

    def get_max_lv(self):
        m = max(self.lv)
        m_i = self.lv.index(m)
        return m_i
    
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
        
        self.count_lv()

        m_i = self.get_max_lv()
        print('max_lv_index:', m_i)
        x_v = (1/self.p_sums[m_i]) * self.get_q_elem_x(m_i)
        y_v = (1/self.p_sums[m_i]) * self.get_q_elem_y(m_i)
        print('x_v=', x_v, 'y_v=', y_v)

        



