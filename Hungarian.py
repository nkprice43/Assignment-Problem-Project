import random
import time
import numpy as np  


class Problem:

    def __init__(self, problemSize: int) -> None:
        self.problemSize = problemSize

        # Initialize a random cost matrix (0 to 1)
        # Using a fixed seed for reproducible results in this example
        random.seed(42)
        self.workers_tasks = [[random.random() for _ in range(self.problemSize)] for _ in range(self.problemSize)]

        # Initial assignments (will be updated by the solver)
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

    # Time taken = time finished - time started
    def start(self):
        self.time = -time.time()

    def stop(self):
        self.time += time.time()

    def totalCost(self):
        cost = 0
        for worker, job in self.assignments:
            # 1 addition, 1 matrix access for each assignment
            cost += self.workers_tasks[worker][job]
            # NOTE: We do not increment basicOpCount here to avoid overcounting if __str__ is called multiple times.
        return cost


# --- Manual Hungarian Algorithm Implementation ---

def _step1_reduce_rows(cost_matrix: np.ndarray, p: 'Problem') -> np.ndarray:
    """Subtracts the minimum value from each row."""
    N = p.problemSize
    for i in range(N):
        min_val = np.min(cost_matrix[i, :])
        # Find minimum: N comparisons/assignments (O(N))
        # Subtract minimum: N subtractions/assignments (O(N))
        cost_matrix[i, :] -= min_val
        p.basicOpCount += 2 * N
    return cost_matrix


def _step2_reduce_cols(cost_matrix: np.ndarray, p: 'Problem') -> np.ndarray:
    """Subtracts the minimum value from each column."""
    N = p.problemSize
    for j in range(N):
        min_val = np.min(cost_matrix[:, j])
        # Find minimum: N comparisons/assignments (O(N))
        # Subtract minimum: N subtractions/assignments (O(N))
        cost_matrix[:, j] -= min_val
        p.basicOpCount += 2 * N
    return cost_matrix


def _step3_cover_zeros(cost_matrix: np.ndarray, p: 'Problem') -> tuple:
    """Tries to cover all zeros with minimum lines."""
    N = p.problemSize
    # Initialize covers and assignments
    row_covered = np.zeros(N, dtype=bool)
    col_covered = np.zeros(N, dtype=bool)
    Z = np.zeros((N, N), dtype=int)  # Zeros matrix

    # Find initial assignments (a single zero in row/col)
    assignments = []

    # Simple assignment heuristic (Greedy, not necessarily optimal for coverage)
    for i in range(N):
        for j in range(N):
            # N*N comparisons
            p.basicOpCount += 1
            if cost_matrix[i, j] == 0 and not row_covered[i] and not col_covered[j]:
                Z[i, j] = 1
                row_covered[i] = True
                col_covered[j] = True
                assignments.append((i, j))
                # 3 assignments (Z[i,j], row_covered, col_covered)
                p.basicOpCount += 3

                # Step 3.1: Cover all columns that contain an assignment (marked Z=1)
    col_covered = np.any(Z, axis=0)

    # The number of lines is the sum of covered rows/columns.
    # The full Hungarian covering logic (Kuhn's modification/Munkres) is complex.
    # We simplify this step by just counting the assigned columns as covered.

    num_lines = np.sum(col_covered)

    # 1 addition/comparison for each element in the array
    p.basicOpCount += N

