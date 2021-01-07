from typing import List
from random import random, randint

Graph = List[List[int]]

def generate_graph(size: int, density: float, min_weight: int = 1, max_weight: int = 1) -> Graph:
    graph = [[0] * size for _ in range(size)]
    for u in range(1, size):
        for v in range(0, u):
            if density > random():
                weight = randint(min_weight, max_weight)
                graph[u][v] = weight
                graph[v][u] = weight

    return graph

def print_graph(graph: Graph) -> None:
    for row in graph:
        print(*row)
