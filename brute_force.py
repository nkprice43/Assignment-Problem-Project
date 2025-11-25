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

def bruteForce(p: Problem) -> Problem:
    p.start()
    it = math.factorial(p.problemSize)

    smallest = math.inf
    keep = p.assignments

    for i in range(it):
        cost = 0
        p.basicOpCount += 1
        for j in range(len(p.workers_tasks)):
            k = (i // (len(p.workers_tasks) ** j)) % len(p.workers_tasks) 
            cost += p.workers_tasks[j][k]
            keep[j] = (j, k)
        if cost < smallest:
            smallest = cost
            p.assignments = keep
    p.stop()
        
    return p

if __name__ == '__main__':
    p = Problem(10)

    bruteForce(p)

    print(p)

