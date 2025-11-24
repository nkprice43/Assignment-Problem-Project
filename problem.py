# This class exists to represent an instance of The Assignment Problem at a given size

import array as arr
import time
import random

class Problem:

    def __init__(self, problemSize: int) -> None:

        self.problemSize = 2 ** problemSize
        
        self.workers = arr.array('d', [random.random() for i in range(self.problemSize)])
        
        self.tasks = arr.array('d', [random.random() for i in range(self.problemSize)])
        
        self.costMatrix = [[random.random() for i in range(self.problemSize)] for j in range(self.problemSize)]
        
        self.assignments = [(i, 0) for i in range(self.problemSize)]
        
        self.time = 0

        self.basicOpCount = 0

    def __str__(self) -> str:
        s = f'''Problem Size: {self.problemSize}
            Workers: {self.workers}
            Tasks: {self.tasks}
            Assignments: {self.assignments}
            Processing Time: {self.time}
        '''

        return s

    # Time taken = time finished - time started
    def start(self):
        self.time = -time.time()

    def stop(self):
        self.time += time.time()

if __name__ == '__main__':
    random.seed(time.time())
    p = Problem(3)
    p.start()
    print(p)
