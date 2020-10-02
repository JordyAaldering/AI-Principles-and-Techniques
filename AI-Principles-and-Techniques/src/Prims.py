from typing import List

from sys import maxsize as Inf

class Prims:

    Graph = List[List[int]]

    def __init__(self, graph: Graph):
        self.graph = graph
        self.size = len(graph)

        self.keys = [Inf] * self.size
        self.parents = [None] * self.size
        self.in_mst = [False] * self.size
        
        self.calculate_mst()
        
    def calculate_mst(self):
        self.keys[0] = 0
        self.parents[0] = -1
 
        for _ in range(self.size):
            u = self.extract_min()

            for v in range(self.size):
                if not self.in_mst[v] and self.graph[u][v] > 0 and self.keys[v] > self.graph[u][v]:
                    self.keys[v] = self.graph[u][v]
                    self.parents[v] = u

    def extract_min(self) -> int:
        min = Inf
        min_index = -1
 
        for v in range(self.size):
            if not self.in_mst[v] and self.keys[v] < min:
                min = self.keys[v]
                min_index = v
 
        self.in_mst[min_index] = True
        return min_index

    def print_mst(self) -> None:
        print("Edge\t Weight")
        for i in range(1, self.size):
            print(self.parents[i], "-", i, "\t", self.graph[i][self.parents[i]])

if __name__ == "__main__":
    graph = [
        [0, 1, 3, 0, 0],
        [1, 0, 2, 0, 0],
        [3, 2, 0, 4, 1],
        [0, 0, 4, 0, 3],
        [0, 0, 1, 3, 0],
    ]

    p = Prims(graph);
    p.print_mst()
