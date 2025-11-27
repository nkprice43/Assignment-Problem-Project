# This class exists to represent an instance of The Assignment Problem at a given size

import time
import random

class Problem:

    def __init__(self, problemSize: int) -> None:

        self.problemSize = problemSize
        
        self.workers_tasks = [[random.random() for _ in range(self.problemSize)] for _ in range(self.problemSize)]
        
        self.assignments = [(i, i) for i in range(self.problemSize)]
        
        self.time = 0

        self.basicOpCount = 0

    def __str__(self) -> str:
        s = f'''
Problem Size: {self.problemSize}
            Total Cost: {self.totalCost()}
            Basic Operation Count: {self.basicOpCount}
            Processing Time: {self.time}
        '''

        return s

    # Time taken = time finished - time started
    def start(self):
        self.time = -time.time()

    def stop(self):
        self.time += time.time()

    def totalCost(self):
        cost = 0
        for a in self.assignments:
            cost += self.workers_tasks[a[0]][a[1]]
        return cost


if __name__ == '__main__':
    random.seed(time.time())
    p = Problem(3)
    p.start()
    p.stop()

    print(p)
