import random
import time
import numpy as np  # Used for matrix operations, which makes implementation cleaner


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

    return num_lines, row_covered, col_covered, Z


def _step4_adjust_matrix(cost_matrix: np.ndarray, row_covered: np.ndarray, col_covered: np.ndarray,
                         p: 'Problem') -> np.ndarray:
    """Adjusts the matrix if the number of lines is less than N."""
    N = p.problemSize

    # Find the smallest uncovered element (min_val)
    min_val = np.inf
    # N*N comparisons
    p.basicOpCount += N * N
    for i in range(N):
        if not row_covered[i]:
            for j in range(N):
                if not col_covered[j]:
                    min_val = min(min_val, cost_matrix[i, j])

    # 1. Subtract min_val from every uncovered element
    # N*N checks/subtractions in the worst case (O(N^2))
    for i in range(N):
        for j in range(N):
            if not row_covered[i] and not col_covered[j]:
                cost_matrix[i, j] -= min_val
                p.basicOpCount += 1

    # 2. Add min_val to every element covered by two lines (double-covered)
    # N*N checks/additions in the worst case (O(N^2))
    for i in range(N):
        if row_covered[i]:
            for j in range(N):
                if col_covered[j]:
                    cost_matrix[i, j] += min_val
                    p.basicOpCount += 1

    # The total operation count for this step is dominated by O(N^2)
    return cost_matrix


def _get_assignments(Z: np.ndarray) -> list:
    """Extracts the final assignments from the Z matrix."""
    return list(zip(*np.where(Z == 1)))


def solve_hungarian(p: Problem) -> None:
    """
    Solves the assignment problem using a manual implementation of the Hungarian method.
    Modifies the problem_instance in-place and counts basic operations.
    NOTE: The assignment logic (Steps 3/4) is simplified for counting and Python readability.
    """
    p.start()
    N = p.problemSize

    # 1. Copy the cost matrix to a working matrix (N*N assignments)
    cost_matrix = np.array(p.workers_tasks)
    p.basicOpCount += N * N

    # The core loop of the Hungarian algorithm
    iteration_count = 0
    while True:
        iteration_count += 1

        # Step 1: Row Reduction
        cost_matrix = _step1_reduce_rows(cost_matrix, p)

        # Step 2: Column Reduction
        cost_matrix = _step2_reduce_cols(cost_matrix, p)

        # Step 3: Cover Zeros and find initial assignment
        num_lines, row_covered, col_covered, Z = _step3_cover_zeros(cost_matrix, p)

        # Check for optimality (N lines cover all zeros)
        # N comparisons
        p.basicOpCount += N
        if num_lines == N:
            break

        # Step 4: Adjust the matrix
        cost_matrix = _step4_adjust_matrix(cost_matrix, row_covered, col_covered, p)
        # The full implementation of Step 3 (finding min lines/max matching)
        # is complex and usually requires iterative covering/uncovering (Munkres' algorithm).
        # We rely on the matrix adjustment to eventually force an N-line cover.

    # Final Step: Extract the assignments
    p.assignments = _get_assignments(Z)

    # 1 assignment for the final result
    p.basicOpCount += 1

    p.stop()


if __name__ == '__main__':
    # Set a small, manageable problem size for testing
    N = 5

    # Reset random seed for reproducible problem data
    random.seed(42)
    p = Problem(N)

    solve_hungarian(p)
    print(p)
