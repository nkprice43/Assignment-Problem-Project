# How to run:
# python main.py

from problem import Problem
import random
import time
from brute_force import bruteForce
from Hungarian import hungarian
from Greedy import solve_greedy
from maxflowreduction import solve_assignment_with_min_cost_flow
import matplotlib.pyplot as plt
from copy import deepcopy

if __name__ == '__main__':

    t = -time.time()

    random.seed(time.time())

    maxSize = 100
    numProbs = maxSize - 2
    maxBF = 8
    reps = 5

    

    problems = [ Problem(i % numProbs + 2) for i in range(0, numProbs * reps) ]
    problemsSet = [ [deepcopy(i) for i in problems], [deepcopy(i) for i in problems], [deepcopy(i) for i in problems], [deepcopy(i) for i in problems] ]

    for i in range(len(problems)):
        print(i)
        # run each algorithm here
        solve_greedy(problemsSet[0][i])
        if i % numProbs < maxBF:
            bruteForce(problemsSet[1][i])
        hungarian(problemsSet[2][i])
        solve_assignment_with_min_cost_flow(problemsSet[3][i])

    problemSizes = [ i.problemSize for i in problems[:numProbs] ]

    greedyTimes = [ 0.0 for _ in range(numProbs) ]

    maxFlowTimes = [ 0.0 for _ in range(numProbs) ]

    hungarianTimes = [ 0.0 for _ in range(numProbs) ]

    bruteForceTimes = [ 0.0 for _ in range(maxBF) ]


    greedyOps = [ 0.0 for _ in range(numProbs) ]

    maxFlowOps = [ 0.0 for _ in range(numProbs) ]

    hungarianOps = [ 0.0 for _ in range(numProbs) ]

    bruteForceOps = [ 0.0 for _ in range(maxBF) ]


    greedySol = [ i.totalCost() for i in problemsSet[0] ]

    maxFlowSol = [ i.totalCost() for i in problemsSet[3] ]

    hungarianSol = [ i.totalCost() for i in problemsSet[2] ]

    bruteForceSol = [ i.totalCost() for i in problemsSet[1] ]

    
    greedyErrorBF = [ 0.0 for _ in range(maxBF) ]
    hungarianErrorBF = [ 0.0 for _ in range(maxBF) ]
    maxFlowErrorBF = [ 0.0 for _ in range(maxBF) ]

    greedyErrorHG = [ 0.0 for _ in range(numProbs) ]
    maxFlowErrorHG = [ 0.0 for _ in range(numProbs) ]

    for i in range(numProbs):
        for j in range(reps):
            greedyTimes[i] += problemsSet[0][i + j * numProbs].time / reps
            if i < maxBF:
                bruteForceTimes[i] += problemsSet[1][i + j * numProbs].time / reps
            hungarianTimes[i] += problemsSet[2][i + j * numProbs].time / reps
            maxFlowTimes[i] += problemsSet[3][i + j * numProbs].time / reps

            greedyOps[i] += problemsSet[0][i + j * numProbs].basicOpCount / reps
            if i < maxBF:
                bruteForceOps[i] += problemsSet[1][i + j * numProbs].basicOpCount / reps
            hungarianOps[i] += problemsSet[2][i + j * numProbs].basicOpCount / reps
            maxFlowOps[i] += problemsSet[3][i + j * numProbs].basicOpCount / reps
            greedyErrorHG[i] += (100 * (greedySol[i + j * numProbs] - hungarianSol[i + j * numProbs]) / hungarianSol[i + j * numProbs]) / reps
            maxFlowErrorHG[i] += (100 * (maxFlowSol[i + j * numProbs] - hungarianSol[i + j * numProbs]) / hungarianSol[i + j * numProbs]) / reps
            if i < maxBF:
                greedyErrorBF[i] += (100 * (greedySol[i + j * numProbs] - bruteForceSol[i + j * numProbs]) / bruteForceSol[i + j * numProbs]) / reps
                hungarianErrorBF[i] += (100 * (hungarianSol[i + j * numProbs] - bruteForceSol[i + j * numProbs]) / bruteForceSol[i + j * numProbs]) / reps
                maxFlowErrorBF[i] += (100 * (maxFlowSol[i + j * numProbs] - bruteForceSol[i + j * numProbs]) / bruteForceSol[i + j * numProbs]) / reps





    aT = plt.figure()
    plt.title('Figure 1\nRun Time vs Problem Size')
    plt.xlabel('Problem Size')
    plt.ylabel('Run Time (s)')
    plt.plot(problemSizes[:maxBF], bruteForceTimes, color='red')
    plt.plot(problemSizes, greedyTimes, color='green')
    plt.plot(problemSizes, hungarianTimes, color='orange')
    plt.plot(problemSizes, maxFlowTimes, color='blue')
    plt.savefig('Figure1.png')

    aO = plt.figure()
    plt.title('Figure 2\nBasic Ops vs Problem Size')
    plt.xlabel('Problem Size')
    plt.ylabel('Basic Operations')
    plt.plot(problemSizes[:maxBF], bruteForceOps, color='red')
    plt.plot(problemSizes, greedyOps, color='green')
    plt.plot(problemSizes, hungarianOps, color='orange')
    plt.plot(problemSizes, maxFlowOps, color='blue')
    plt.savefig('Figure2.png')

    xT = plt.figure()
    plt.title('Figure 3\nRun Time vs Problem Size (w/o BF)')
    plt.xlabel('Problem Size')
    plt.ylabel('Run Time (s)')
    plt.plot(problemSizes, greedyTimes, color='green')
    plt.plot(problemSizes, hungarianTimes, color='orange')
    plt.plot(problemSizes, maxFlowTimes, color='blue')
    plt.savefig('Figure3.png')

    xO = plt.figure()
    plt.title('Figure 4\nBasic Ops vs Problem Size (w/o BF)')
    plt.xlabel('Problem Size')
    plt.ylabel('Basic Operations')
    plt.plot(problemSizes, greedyOps, color='green')
    plt.plot(problemSizes, hungarianOps, color='orange')
    plt.plot(problemSizes, maxFlowOps, color='blue')
    plt.savefig('Figure4.png')

    pctDiffBF = plt.figure()
    plt.title('Figure 5\nPercent Error vs Problem Size (vs BF)')
    plt.xlabel('Problem Size')
    plt.ylabel('Percent Error (%)')
    plt.plot(problemSizes[:len(greedyErrorBF)], greedyErrorBF, color='green')
    plt.plot(problemSizes[:len(hungarianErrorBF)], hungarianErrorBF, color='orange')
    plt.plot(problemSizes[:len(maxFlowErrorBF)], maxFlowErrorBF, color='blue')
    plt.savefig('Figure5.png')
    
    pctDiffHG = plt.figure()
    plt.title('Figure 6\nPercent Error vs Problem Size (vs HG)')
    plt.xlabel('Problem Size')
    plt.ylabel('Percent Error (%)')
    plt.plot(problemSizes, greedyErrorHG, color='green')
    plt.plot(problemSizes, maxFlowErrorHG, color='blue')
    plt.savefig('Figure6.png')
    



    t += time.time()
    print(f'{t} seconds')

    plt.show()
