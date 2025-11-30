#Brute Force Assignment Problem

'''
workers
0 0 0 0 0 0

0 0 0 0 0 0 t
            a
0 0 0 0 0 0 s
            k
0 0 0 0 0 0 s

0 0 0 0 0 0

'''

import math

from problem import Problem

def isMobile(idx: int, l: list, d: list) -> bool:
    idx2 = idx + d[idx]
    if idx2 >= 0 and idx2 < len(l):
        return l[idx] > l[idx2]
    return False

def jt(p: list[list], mobile: list = [], d: list | None = None, rec: bool = False):

    l = p[-1].copy()
    
    if d == None:
        d = [ -1 for _ in l]

    if not rec:
        for i in range(len(l)):
            if isMobile(i, l, d):
                mobile.append(l[i])
        while len(mobile) > 0:
            p, mobile, d = jt(p, mobile, d, True)
        return p, mobile, d
    else:

        mobile = []
        for i in range(len(l)):
            if isMobile(i, l, d):
                mobile.append(l[i])

        if len(mobile) == 0:
            return p

        m = max(mobile)
        mi = l.index(m)
        dm = d[mi]

        l.pop(mi)
        l.insert(mi + d[mi], m)

        d.pop(mi)
        d.insert(mi + dm, dm)

        for i in range(len(l)):
            if l[i] > m:
                d[i] *= -1

        mobile = []
        for i in range(len(l)):
            if isMobile(i, l, d):
                mobile.append(l[i])

        p.append(l)

        return p, mobile, d




def bruteForce(p: Problem) -> None:
    p.start()
    perms, _, _ = jt([list(range(0, p.problemSize))])

    smallest = math.inf
    keep = p.assignments

    for i in perms:
        cost = 0
        p.basicOpCount += 1
        for j in range(len(p.workers_tasks)):
            k = i[j]
            cost += p.workers_tasks[j][k]
            keep[j] = (j, k)
        if cost < smallest:
            p.assignments = keep.copy()
            smallest = cost
    p.stop()
        
    #return p

if __name__ == '__main__':
    p = Problem(3)

    bruteForce(p)

    print(p)

