from problem import Problem
from brute_force import bruteForce
from Hungarian import solve_hungarian
from Greedy import solve_greedy
from maxflowreduction import solve_assignment_with_min_cost_flow, assign_solution_to_problem
import matplotlib.pyplot as plt
from copy import deepcopy

if __name__ == '__main__':

    maxSize = 10

    problems = [ Problem(i) for i in range(2, maxSize) ]
    problemsSet = [ [deepcopy(i) for i in problems], [deepcopy(i) for i in problems], [deepcopy(i) for i in problems], [deepcopy(i) for i in problems] ]

    for i in range(len(problems)):
        # run each algorithm here
        solve_greedy(problemsSet[0][i])
        bruteForce(problemsSet[1][i])
        solve_hungarian(problemsSet[2][i])
        problemsSet[3][i].start()
        a, b = solve_assignment_with_min_cost_flow(problemsSet[3][i])
        assign_solution_to_problem(problemsSet[3][i], a, b)
        problemsSet[3][i].stop()
        print(problemsSet[0][i])
        print(problemsSet[1][i])
        print(problemsSet[2][i])
        print(problemsSet[3][i])
