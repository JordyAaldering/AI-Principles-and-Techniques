from Prims import *

from random import random, randint

def generate_graph(size: int, density: float) -> Graph:
    graph = [[0] * size for _ in range(size)]
    for u in range(1, size):
        for v in range(0, u):
            if density > random():
                weight = randint(1, size)
                graph[u][v] = weight
                graph[v][u] = weight

    return graph

def print_graph(graph: Graph) -> None:
    for row in graph:
        print(*row)

if __name__ == "__main__":
    graph = generate_graph(10, 0.5)
    parents = prims_mst(graph)

    print_graph(graph)
    print_mst(graph, parents)
