from Prims import Prims

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
