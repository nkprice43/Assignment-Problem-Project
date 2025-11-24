import problem
import brute_force

if __name__ == '__main__':

    maxSize = 10

    problems = [ problem.Problem(i) for i in range(maxSize) ]

    for i in problems:
        print(i)
