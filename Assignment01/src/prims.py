from graph import *
from sys import maxsize as Inf

def prims_mst(graph: Graph, root: int = 0) -> List[int]:
    size = len(graph)
    keys = [Inf] * size
    parents = [-1] * size
    in_mst = [False] * size
    
    keys[root] = 0

    for _ in range(size):
        u = extract_min(keys, in_mst)

        for v in range(size):
            if not in_mst[v] and graph[u][v] > 0 and keys[v] > graph[u][v]:
                keys[v] = graph[u][v]
                parents[v] = u

    return parents

def extract_min(keys: List[int], in_mst: List[bool]) -> int:
    min_weight = Inf
    min_index = -1
 
    for v in range(len(keys)):
        if not in_mst[v] and keys[v] < min_weight:
            min_weight = keys[v]
            min_index = v
 
    in_mst[min_index] = True
    return min_index

def print_mst(graph: Graph, parents: List[int]) -> None:
    print("Edge\t Weight")
    for i in range(len(graph)):
        if parents[i] >= 0:
            print(parents[i], "to", i, "\t", graph[i][parents[i]])
