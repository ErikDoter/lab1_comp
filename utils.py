from copy import copy
from typing import List


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

    print(r)
    print(lm)
    print(l)
    lm.sort()
    i = 0 
    while sum(r) < s:
        r.append(lm[-1])
        #print(sum(r))
    if sum(r) == s:
        return r
    r.pop()
    lm.pop()
    return recursion(s=s, l=l, r=r, lm=lm)

print(recursion(250, [45,55,70,80]))
