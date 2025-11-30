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

    random.seed(time.time())

    maxSize = 50
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


    greedySol = [ i.totalCost() for i in problemsSet[0] ]

    maxFlowSol = [ i.totalCost() for i in problemsSet[3] ]

    hungarianSol = [ i.totalCost() for i in problemsSet[2] ]

    bruteForceSol = [ i.totalCost() for i in problemsSet[1] ]

    '''bfT = plt.figure()
    plt.plot(problemSizes[:maxBF], bruteForceTimes)
    
    bfO = plt.figure()
    plt.plot(problemSizes[:maxBF], bruteForceOps)
    
    gdT = plt.figure()
    plt.plot(problemSizes, greedyTimes)
    
    gdO = plt.figure()
    plt.plot(problemSizes, greedyOps)
      
    hgT = plt.figure()
    plt.plot(problemSizes, hungarianTimes)
    
    hgO = plt.figure()
    plt.plot(problemSizes, hungarianOps)
    
    mfT = plt.figure()
    plt.plot(problemSizes, maxFlowTimes)
    
    mfO = plt.figure()
    plt.plot(problemSizes, maxFlowOps)'''

    aT = plt.figure()
    plt.title('Run Time vs Problem Size')
    plt.plot(problemSizes[:maxBF], bruteForceTimes, color='red')
    plt.plot(problemSizes, greedyTimes, color='green')
    plt.plot(problemSizes, hungarianTimes, color='orange')
    plt.plot(problemSizes, maxFlowTimes, color='blue')

    aO = plt.figure()
    plt.title('Basic Ops vs Problem Size')
    plt.plot(problemSizes[:maxBF], bruteForceOps, color='red')
    plt.plot(problemSizes, greedyOps, color='green')
    plt.plot(problemSizes, hungarianOps, color='orange')
    plt.plot(problemSizes, maxFlowOps, color='blue')

    xT = plt.figure()
    plt.title('Run Time vs Problem Size (w/o BF)')
    plt.plot(problemSizes, greedyTimes, color='green')
    plt.plot(problemSizes, hungarianTimes, color='orange')
    plt.plot(problemSizes, maxFlowTimes, color='blue')

    xO = plt.figure()
    plt.title('Basic Ops vs Problem Size (w/o BF)')
    plt.plot(problemSizes, greedyOps, color='green')
    plt.plot(problemSizes, hungarianOps, color='orange')
    plt.plot(problemSizes, maxFlowOps, color='blue')



    plt.show()
