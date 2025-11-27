import numpy as np
from scipy.optimize import linear_sum_assignment

from problem import Problem

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
