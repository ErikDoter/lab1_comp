from copy import copy
from hashlib import new
from operator import isub
from numpy import append, mat
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

        max_k = -100000
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
    
    def get_index_in_plata(self, elem: int): #???????????????????? ???? ??????????
        for i, x in enumerate(self.plata):
            if elem in x:
                return (i, x.index(elem))

    def get_q_elem(self, elem: int): #?????????????? q ?????? ????????????????
        x, y = self.get_index_in_plata(elem=elem)
        sum_q_for_el = 0
        for i, row in enumerate(self.plata):
            for j, col in enumerate(row): 
                        s = math.fabs(x-j) + math.fabs(y-i)
                        sum_q_for_el += self.matrix[col][elem] * s

        return sum_q_for_el

    def get_q_elem_x(self, elem: int): #?????????????? q ?????? ???????????????????? ???? x
        x, y = self.get_index_in_plata(elem=elem)
        sum_q_for_el = 0
        for i, row in enumerate(self.plata):
            for j, col in enumerate(row):
                        s = j - x
                        sum_q_for_el += self.matrix[col][elem] * s

        return sum_q_for_el

    
    def get_q_elem_y(self, elem: int): #?????????????? q ?????? ???????????????????? ???? y
        x, y = self.get_index_in_plata(elem=elem)
        sum_q_for_el = 0
        for i, row in enumerate(self.plata):
            for j, col in enumerate(row):
                        s = i - y
                        sum_q_for_el += self.matrix[col][elem] * s

        return sum_q_for_el
        
    
    def count_lv(self, plata, s = ''): #???????????? lv ?????? ???????? ??????????????????
        for i, row in enumerate(plata):
            for j, col in enumerate(row):
                self.lv[col] = (1/self.p_sums[col]) * self.get_q_elem(col)
        print(f'lv {s}:', self.lv)

    def get_max_lv(self):
        m = max(self.lv)
        m_i = self.lv.index(m)
        return m_i

    def compare_list(self, a, b):
        if len(a) != len(b):
            return False
        for i1, _ in enumerate(a):
            if a[i1] != b[i1]:
                return False
        return True

    def get_list_to_swap(self, coords: list, ignore):
        res = []
        res.append([math.ceil(coords[0]), math.ceil(coords[1])])
        res.append([math.ceil(coords[0]), math.floor(coords[1])])
        res.append([math.floor(coords[0]), math.ceil(coords[1])])
        res.append([math.floor(coords[0]), math.floor(coords[1])])
        res.append([0,0])
        for i1, r1 in enumerate(res):
            for i2 in range(i1+1, len(res)):
                if self.compare_list(res[i1], res[i2]):
                    res.pop(i2)
        for i, element in enumerate(res):
            if element[0] == ignore[0] and element[1] == ignore[1]:
                res.pop(i)
        return res


    
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
        
        flag = True

        while flag:
        
            self.count_lv(self.plata)

            m_i = self.get_max_lv()
            print('max_lv_index:', m_i)
            x_v = (1/self.p_sums[m_i]) * self.get_q_elem_x(m_i)
            y_v = (1/self.p_sums[m_i]) * self.get_q_elem_y(m_i)
            print('x_v=', x_v, 'y_v=', y_v)
            cord_max_lv = list(self.get_index_in_plata(m_i))
            x_offset = cord_max_lv[1] + x_v
            y_offset = cord_max_lv[0] + y_v
            list_to_swap = self.get_list_to_swap([y_offset, x_offset], cord_max_lv)
            print('list_to_swap',list_to_swap)
            delta_l = [0] * len(list_to_swap)
            for index, swap in enumerate(list_to_swap):
                new_plata = []
                for pl in self.plata:
                    new_plata_row = []
                    for p in pl:
                        new_plata_row.append(p)
                    new_plata.append(new_plata_row)
                l_from_old = self.lv[self.plata[cord_max_lv[0]][cord_max_lv[1]]]
                l_to_old = self.lv[self.plata[swap[0]][swap[1]]]
                new_plata[cord_max_lv[0]][cord_max_lv[1]], new_plata[swap[0]][swap[1]] = new_plata[swap[0]][swap[1]], new_plata[cord_max_lv[0]][cord_max_lv[1]]
                self.count_lv(plata = new_plata, s='new')
                l_from_new = self.lv[self.plata[cord_max_lv[0]][cord_max_lv[1]]] 
                l_to_new = self.lv[self.plata[cord_max_lv[0]][cord_max_lv[1]]]
                delta_l[index] = (l_from_old + l_to_old) - l_from_new - l_to_new
                self.count_lv(self.plata)
            max_delta_l = max(delta_l)
            max_delta_l_index = delta_l.index(max_delta_l)
            print('delta_l:', delta_l)
            if max_delta_l > 0:
                swap = list_to_swap[max_delta_l_index]
                print('swap', cord_max_lv, 'to', swap)
                print('swap', self.plata[cord_max_lv[0]][cord_max_lv[1]], 'to', self.plata[swap[0]][swap[1]])
                print('max_delta_l_index:', max_delta_l_index)
                self.plata[cord_max_lv[0]][cord_max_lv[1]], self.plata[swap[0]][swap[1]] = self.plata[swap[0]][swap[1]], self.plata[cord_max_lv[0]][cord_max_lv[1]]
            else:
                flag = False

            for p in self.plata:
                print(p)


        



