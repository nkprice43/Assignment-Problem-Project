from problem import Problem
import brute_force
import matplotlib.pyplot as plt

if __name__ == '__main__':

    maxSize = 10

    problems = [ Problem(i) for i in range(1, maxSize) ]
    problemsSet = [ problems, problems, problems, problems ]

    for i in problems:
        # run each algorithm here
        i.start()
        i.stop()
        print(i)

    sizes = [ i.problemSize for i in problems]
    times = [ i.time for i in problems ]

    plt.plot(sizes, times)
    plt.show()
