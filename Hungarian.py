import numpy as np
import random
import time
from scipy.optimize import linear_sum_assignment

class Problem:

    def __init__(self, problemSize: int) -> None:
        self.problemSize = problemSize
        # Initialize a random cost matrix (0 to 1)
        self.workers_tasks = [[random.random() for i in range(self.problemSize)] for j in range(self.problemSize)]
        # Initial assignments (will be updated by the solver)
        self.assignments = []
        self.time = 0.0
        self.basicOpCount = 0  # Note: SciPy library operations are not easily counted

    def __str__(self) -> str:
        s = f'''
    Problem Size: {self.problemSize}
                Total Cost: {self.totalCost()}
                Basic Operation Count: {self.basicOpCount}
                Processing Time: {self.time:.6f} seconds
            '''
        return s

    def start(self):
        self.time = -time.time()

    def stop(self):
        self.time += time.time()

    def totalCost(self):
        cost = 0
        for worker, job in self.assignments:
            cost += self.workers_tasks[worker][job]
        return cost


def solve_hungarian(p: Problem) -> None:
    """
    Solves the assignment problem for a given Problem instance using the
    Hungarian algorithm via scipy.optimize.linear_sum_assignment.
    Modifies the problem_instance in-place.
    """
    p.start()

    # Convert cost matrix to a NumPy array, which SciPy expects
    cost_matrix = np.array(p.workers_tasks)

    # The linear_sum_assignment function returns the optimal row and column indices
    # (worker_indices, job_indices)
    worker_indices, job_indices = linear_sum_assignment(cost_matrix)

    # Format the results into a list of tuples (worker, job)
    assignments = list(zip(worker_indices, job_indices))

    # Update the Problem instance with the optimal results
    p.assignments = assignments

    # Note: Counting basic operations within SciPy's optimized C/Fortran code
    # is not feasible from Python. We leave basicOpCount as 0 or a placeholder.
    # problem_instance.basicOpCount = ...

    p.stop()


if __name__ == '__main__':
    p = Problem(10)

    solve_hungarian(p)

    print(p)