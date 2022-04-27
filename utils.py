from copy import copy
from tkinter import N
from typing import List
from numpy import rec

from pyrsistent import b


def rec3(s:int, l: List[int]):
    res = []
    def recursion(s:int, l: List[int], r=[], lm=[]) -> List[int] :
        rofl = -1
        if len(lm)==0 and len(r) !=0:
            rofl = r.pop()
        if len(lm)==0:
            if rofl == -1:
                lm = copy(l)
            else:
                for i in l:
                    if i < rofl:
                        lm.append(i)

        lm.sort()
        i = 0 
        while sum(r) < s:
            r.append(lm[-1])
        if sum(r) == s and r not in res:
            print(r)
            print(f'l={l}')
            print(f'lm={lm}')
            res.append(r)
            return
        r.pop()
        lm.pop()
        return recursion(s=s, l=l, r=r, lm=lm)

    
    recursion(s=s, l=l)
    return res


def rec(s: int, init_l: List[int]):
    res = []

    def rec2(s: int, init_l: List[int], b = []):
        sum_buf = sum(b)
        if sum_buf < s:
            #print('<',b)
            for elem_l in init_l:
                c = copy(b)
                c.append(elem_l)
                r=rec2(s=s, init_l=init_l, b=c)
                if isinstance(r, list):
                    #print(r)
                    r.sort()
                    if r not in res:
                        res.append(r)
                        print(len(res))
        elif sum_buf == s:
            #print('=', b)
            return b
        else:
            return -1
    init_l.sort(reverse=True)
    rec2(s=s, init_l=init_l)
    return res
            
        
print('res=',rec(20, [3,4,5,7]))

