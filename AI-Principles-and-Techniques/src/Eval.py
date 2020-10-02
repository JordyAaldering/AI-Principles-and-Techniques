from Prims import *
from Graph import *

import matplotlib.pyplot as plt
from time import time

STEPS = 20
REPEATS = 10
STEP_SIZE = 100
STEP_WEIGHT = 1000

def eval_vertices():
    sizes = [0] * STEPS
    timings = [0.0] * STEPS

    for i in range(STEPS):
        size = (i + 1) * STEP_SIZE
        graph = generate_graph(size, 0.5)

        start_time = time()
        parents = prims_mst(graph)
        timings[i] = int((time() - start_time) * 1000)
        sizes[i] = size

    plt.plot(sizes, timings)
    plt.title("Runtime for increasing graph sizes")
    plt.xlabel("Vertices")
    plt.ylabel("Time (ms)")
    plt.xlim(STEP_SIZE, STEP_SIZE * STEPS)
    plt.ylim(bottom=0.0)
    plt.savefig("../images/vertices")
    plt.close()

def eval_density():
    densities = [0.0] * STEPS
    timings = [0.0] * STEPS

    for i in range(STEPS):
        density = i / (STEPS - 1)
        i_timings = [0.0] * REPEATS

        for r in range(REPEATS):
            graph = generate_graph(100, density)

            start_time = time()
            parents = prims_mst(graph)
            i_timings[r] = int((time() - start_time) * 1000)
            
        densities[i] = density
        timings[i] = sum(i_timings) / REPEATS

    plt.plot(densities, timings)
    plt.title("Runtime for increasing density")
    plt.xlabel("Density")
    plt.ylabel("Time (ms)")
    plt.xlim(0.0, 1.0)
    plt.ylim(bottom=0.0)
    plt.savefig("../images/density")
    plt.close()

def eval_weight_range():
    timings = []

    for weight in [Inf, 2, 1]:
        i_timings = [0.0] * REPEATS
        for r in range(REPEATS):
            graph = generate_graph(100, 0.5, max_weight=weight)

            start_time = time()
            parents = prims_mst(graph)
            i_timings[r] = int((time() - start_time) * 1000)
            
        timings.append(sum(i_timings) / REPEATS)

    plt.bar(["0%", "50%", "100%"], timings)
    plt.title("Runtime for distribution of edge weights")
    plt.xlabel("Percentage of equal weights")
    plt.ylabel("Time (ms)")
    plt.savefig("../images/weight_range")
    plt.close()

def eval_weight_magnitude():
    magnitudes = [[1,2], [100,1000], [1000,10000]]
    labels = ["1, 2", "100, 1000", "1000, 10000"]
    timings = []

    for weight in magnitudes:
        i_timings = [0.0] * REPEATS

        for r in range(REPEATS):
            graph = generate_graph(100, 0.5, min_weight=weight[0], max_weight=weight[1])

            start_time = time()
            parents = prims_mst(graph)
            i_timings[r] = int((time() - start_time) * 1000)
            
        timings.append(sum(i_timings) / REPEATS)

    plt.bar(labels, timings)
    plt.title("Runtime for increasing edge magnitudes")
    plt.xlabel("Weight range")
    plt.ylabel("Time (ms)")
    plt.savefig("../images/weight_magnitude")
    plt.close()

def eval_weight_max():
    weights = [0.0] * STEPS
    timings = [0.0] * STEPS

    for i in range(STEPS):
        weight = i * STEP_WEIGHT
        i_timings = [0.0] * REPEATS

        for r in range(REPEATS):
            graph = generate_graph(100, weight)

            start_time = time()
            parents = prims_mst(graph)
            i_timings[r] = int((time() - start_time) * 1000)
            
        weights[i] = weight
        timings[i] = sum(i_timings) / REPEATS

    plt.plot(weights, timings)
    plt.title("Runtime for increasing maximum edge weight")
    plt.xlabel("Maximum edge weight")
    plt.ylabel("Time (ms)")
    plt.xlim(0, STEP_WEIGHT * (STEPS - 1))
    plt.ylim(bottom=0.0)
    plt.savefig("../images/weight_max")
    plt.close()

if __name__ == "__main__":
    eval_vertices()
    eval_density()
    eval_weight_range()
    eval_weight_magnitude()
    eval_weight_max()
