import random
import time
import numpy as np

class Problem:
    def __init__(self, problemSize: int) -> None:
        self.problemSize = problemSize
        # Initialize a random cost matrix (0 to 1)
        self.workers_tasks = [[random.random() for i in range(self.problemSize)] for j in range(self.problemSize)]
        # Initial assignments (placeholder)
        self.assignments = []
        self.time = 0.0
        self.basicOpCount = 0

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
        for a in self.assignments:
            cost += self.workers_tasks[a[0]][a[1]]
        return cost


def solve_greedy(p: Problem) -> None:
    """
    Solves the assignment problem for a given Problem instance using a greedy method.
    Modifies the problem_instance in-place.
    """
    p.start()

    # Use a copy of the cost matrix to mark cells as "used"
    matrix = np.array(p.workers_tasks, dtype=float)
    n = p.problemSize
    assignments = []
    basic_ops = 0

    for _ in range(n):
        # Find the index of the minimum element in the remaining matrix
        min_idx_flat = np.argmin(matrix)
        row_idx, col_idx = np.unravel_index(min_idx_flat, matrix.shape)

        # Record the assignment
        assignments.append((row_idx, col_idx))

        # Mark the assigned row and column as "taken" by setting their values to infinity
        matrix[row_idx, :] = np.inf
        matrix[:, col_idx] = np.inf

        # Increment basic operations count
        # Finding the min in a matrix of size roughly n*n is an operation
        basic_ops += n * n

        # Update the Problem instance with results
    p.assignments = assignments
    p.basicOpCount = basic_ops
    p.stop()


if __name__ == '__main__':
    p = Problem(10)

    solve_greedy(p)

    print(p)