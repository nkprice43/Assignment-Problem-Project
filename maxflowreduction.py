import time
import heapq
import random
from typing import List, Tuple
from problem import Problem


class MinCostMaxFlow:
    class Edge:
        __slots__ = ("to", "rev", "cap", "cost")
        def __init__(self, to:int, rev:int, cap:int, cost:float):
            self.to = to
            self.rev = rev
            self.cap = cap
            self.cost = cost

    def __init__(self, n:int):
        self.n = n
        self.graph: List[List[MinCostMaxFlow.Edge]] = [[] for _ in range(n)]

    def add_edge(self, fr:int, to:int, cap:int, cost:float):
        # forward edge
        fwd = MinCostMaxFlow.Edge(to, len(self.graph[to]), cap, cost)
        # reverse edge
        rev = MinCostMaxFlow.Edge(fr, len(self.graph[fr]), 0, -cost)
        self.graph[fr].append(fwd)
        self.graph[to].append(rev)

    def min_cost_flow(self, s:int, t:int, maxf:int):
        n = self.n
        prevv = [0]*n   # previous vertex
        preve = [0]*n   # previous edge index
        INF = float('inf')

        # potentials to deal with negative costs (Johnson)
        pot = [0.0]*n
        dist = [0.0]*n
        flow = 0
        cost = 0.0

        while flow < maxf:
            # Dijkstra on reduced costs
            for i in range(n):
                dist[i] = INF
            dist[s] = 0.0
            pq = [(0.0, s)]
            while pq:
                d, v = heapq.heappop(pq)
                if d > dist[v]:
                    continue
                for ei, e in enumerate(self.graph[v]):
                    if e.cap > 0:
                        nd = dist[v] + e.cost + pot[v] - pot[e.to]
                        if nd < dist[e.to]:
                            dist[e.to] = nd
                            prevv[e.to] = v
                            preve[e.to] = ei
                            heapq.heappush(pq, (nd, e.to))
            if dist[t] == INF:
                # cannot send more flow
                break
            # update potentials
            for v in range(n):
                if dist[v] < INF:
                    pot[v] += dist[v]
            # add as much as possible (in our construction capacities are 1)
            addf = maxf - flow
            v = t
            while v != s:
                e = self.graph[prevv[v]][preve[v]]
                addf = min(addf, e.cap)
                v = prevv[v]
            v = t
            while v != s:
                e = self.graph[prevv[v]][preve[v]]
                e.cap -= addf
                # reverse edge
                self.graph[v][e.rev].cap += addf
                v = prevv[v]
            # increase totals
            delta_cost = addf * pot[t]
            flow += addf
            cost += delta_cost
        return flow, cost

# -----------------------------
# Build assignment flow network and run min-cost flow
# -----------------------------
def solve_assignment_with_min_cost_flow(p: Problem, require_perfect: bool = True) -> Tuple[List[Tuple[int,int]], float]:
    """
    Given a Problem instance p, builds a flow network and computes a minimum-cost assignment.
    Returns the list of assignments (worker, job) and the total cost.
    If require_perfect is True, raises a ValueError if a perfect assignment (flow = n) cannot be found.
    """

    n = 2 ** p.problemSize
    # node indexing:
    # 0              -> source
    # 1 .. n         -> workers (worker i at node 1+i)
    # n+1 .. 2n      -> jobs (job j at node 1+n+j)
    # 2n+1           -> sink
    S = 0
    worker_base = 1
    job_base = 1 + n
    T = 1 + 2*n
    N = T + 1

    mcmf = MinCostMaxFlow(N)

    # Source -> each worker (cap 1, cost 0)
    for i in range(n):
        mcmf.add_edge(S, worker_base + i, 1, 0.0)

    # Each job -> Sink (cap 1, cost 0)
    for j in range(n):
        mcmf.add_edge(job_base + j, T, 1, 0.0)

    # Worker -> Job edges with cost = p.workers_tasks[i][j], cap 1
    for i in range(n):
        row = p.workers_tasks[i]
        for j in range(n):
            cost_ij = float(row[j])
            mcmf.add_edge(worker_base + i, job_base + j, 1, cost_ij)

    # Run min cost flow asking for flow = n
    desired_flow = n
    flow, total_cost = mcmf.min_cost_flow(S, T, desired_flow)

    if require_perfect and flow < desired_flow:
        raise ValueError(f"Could not find perfect assignment: flow={flow} < {desired_flow}")

    # Extract assignments from residual graph: an edge worker->job that has reverse cap == 1 (meaning it was used)
    assignments = []
    for i in range(n):
        wnode = worker_base + i
        for e in mcmf.graph[wnode]:
            # if edge goes to a job node and its capacity was reduced (i.e., reverse edge has cap 1),
            # then that edge was used in the final flow
            if job_base <= e.to < job_base + n:
                rev_edge = mcmf.graph[e.to][e.rev]
                # If the reverse edge has cap > 0, it means flow was sent in forward direction.
                # For unit capacities, reverse cap == 1 indicates assignment.
                if rev_edge.cap > 0:
                    job_index = e.to - job_base
                    assignments.append((i, job_index))
                    break

    return assignments, total_cost

# -----------------------------
# Utility to update Problem object after solving
# -----------------------------
def assign_solution_to_problem(p: Problem, assignments: List[Tuple[int,int]], cost: float):
    p.assignments = assignments
    # update basicOpCount: count number of assignments as a simple op metric + maybe edges considered
    # We'll set basicOpCount to len(assignments) for simplicity (you can expand this if you want).
    p.basicOpCount = len(assignments)

# -----------------------------
# Example usage (main)
# -----------------------------
if __name__ == "__main__":
    random.seed(time.time())
    p = Problem(3)   # problemSize = 3 -> n = 8

    p.start()
    assignments, cost = solve_assignment_with_min_cost_flow(p, require_perfect=True)
    assign_solution_to_problem(p, assignments, cost)
    p.stop()

    # Print result
    print("Assignments (worker -> job):")
    for w, j in p.assignments:
        print(f"  {w} -> {j}   cost = {p.workers_tasks[w][j]:.6f}")
    print()
    print(p)