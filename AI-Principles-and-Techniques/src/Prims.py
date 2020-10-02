from typing import List
from sys import maxsize as Inf

def extract_min(keys: List[int], in_mst: List[bool]) -> int:
    min = Inf
    min_index = -1
 
    for v in range(len(keys)):
        if keys[v] < min and not in_mst[v]:
            min = keys[v]
            min_index = v
 
    in_mst[min_index] = True
    return min_index

def print_mst(graph, parents):
    print("Edge\t Weight")
    for i in range(1, len(parents)):
        print(parents[i], "-", i, "\t", graph[i][parents[i]])

def prims(graph: List[List[int]]):
    size = len(graph)
    keys = [Inf] * size
    parents = [None] * size
    in_mst = [False] * size
 
    keys[0] = 0
    parents[0] = -1
 
    for _ in range(size):
        u = extract_min(keys, in_mst)

        for v in range(size):
            if graph[u][v] > 0 and not in_mst[v] and keys[v] > graph[u][v]:
                keys[v] = graph[u][v]
                parents[v] = u
 
    print_mst(graph, parents)

if __name__ == "__main__":
    graph = [
        [0, 1, 3, 0, 0],
        [1, 0, 2, 0, 0],
        [3, 2, 0, 4, 1],
        [0, 0, 4, 0, 3],
        [0, 0, 1, 3, 0],
    ]
    prims(graph)
