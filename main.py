from problem import Problem
from brute_force import bruteForce
from Hungarian import solve_hungarian
from Greedy import solve_greedy
import matplotlib.pyplot as plt
from copy import deepcopy

if __name__ == '__main__':

    maxSize = 8

    problems = [ Problem(i) for i in range(2, maxSize) ]
    problemsSet = [ [deepcopy(i) for i in problems], [deepcopy(i) for i in problems], [deepcopy(i) for i in problems], [deepcopy(i) for i in problems] ]

    for i in range(len(problems)):
        # run each algorithm here
        bruteForce(problemsSet[0][i])
        solve_hungarian(problemsSet[1][i])
        solve_greedy(problemsSet[2][i])
        print(problemsSet[0][i])
        print(problemsSet[1][i])
        print(problemsSet[2][i])
