import random
import time
import math
from problem import Problem

def hungarian(problem: Problem):
    problem.start()

    # Copy cost matrix
    C = [row[:] for row in problem.workers_tasks]
    n = problem.problemSize

    # STEP 1: Row reduction
    for i in range(n):
        rmin = min(C[i])
        for j in range(n):
            C[i][j] -= rmin
            problem.basicOpCount += 1

    # STEP 2: Column reduction
    for j in range(n):
        cmin = min(C[i][j] for i in range(n))
        for i in range(n):
            C[i][j] -= cmin
            problem.basicOpCount += 1

    # Masks
    starred = [[False]*n for _ in range(n)]
    primed  = [[False]*n for _ in range(n)]
    row_cover = [False]*n
    col_cover = [False]*n

    # STEP 3: Star zeros
    for i in range(n):
        for j in range(n):
            if C[i][j] == 0 and not row_cover[i] and not col_cover[j]:
                starred[i][j] = True
                row_cover[i] = True
                col_cover[j] = True

    # Uncover rows and columns
    row_cover[:] = [False]*n
    col_cover[:] = [False]*n

    # Helper functions
    def find_star_in_row(r):
        for j in range(n):
            if starred[r][j]: return j
        return None

    def find_star_in_col(c):
        for i in range(n):
            if starred[i][c]: return i
        return None

    def find_prime_in_row(r):
        for j in range(n):
            if primed[r][j]: return j
        return None

    # MAIN LOOP
    while True:

        # STEP 4: Cover columns containing stars
        for i in range(n):
            for j in range(n):
                if starred[i][j]:
                    col_cover[j] = True

        if sum(col_cover) == n:
            break  # Done

        # STEP 5: Find uncovered zero and prime it
        while True:
            z = None
            for i in range(n):
                if not row_cover[i]:
                    for j in range(n):
                        if C[i][j] == 0 and not col_cover[j]:
                            z = (i, j)
                            break
                    if z:
                        break

            if z is None:
                # STEP 7: Adjust matrix
                uncovered_vals = [
                    C[i][j]
                    for i in range(n) if not row_cover[i]
                    for j in range(n) if not col_cover[j]
                ]
                m = min(uncovered_vals)

                for i in range(n):
                    for j in range(n):
                        if row_cover[i]:
                            C[i][j] += m
                        if not col_cover[j]:
                            C[i][j] -= m
                continue

            r, c = z
            primed[r][c] = True

            s = find_star_in_row(r)
            if s is None:
                # STEP 6: Augmenting path
                path = [(r, c)]
                done = False
                while not done:
                    r2 = find_star_in_col(path[-1][1])
                    if r2 is None:
                        done = True
                    else:
                        path.append((r2, path[-1][1]))
                        c2 = find_prime_in_row(r2)
                        path.append((r2, c2))

                # Flip stars along path
                for (r, c) in path:
                    starred[r][c] = not starred[r][c]

                # Clear covers and primes
                row_cover[:] = [False]*n
                col_cover[:] = [False]*n
                primed = [[False]*n for _ in range(n)]

                break  # Return to Step 4

            else:
                row_cover[r] = True
                col_cover[s] = False

    # Final assignments
    assignments = []
    for i in range(n):
        for j in range(n):
            if starred[i][j]:
                assignments.append((i, j))

    problem.assignments = assignments
    problem.stop()

def solve_hungarian(problem: Problem):
    """
    Wrapper that main.py will call.
    """
    hungarian(problem)

"Source: ChatGPT. Version 5.1, OpenAI, 2025, https://chat.openai.com/. Accessed 11/29/25"