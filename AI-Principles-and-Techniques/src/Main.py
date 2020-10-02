from Prims import *
from Graph import *

if __name__ == "__main__":
    graph = generate_graph(10, 0.5)
    parents = prims_mst(graph)

    print_graph(graph)
    print_mst(graph, parents)
