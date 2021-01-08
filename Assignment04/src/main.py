from grid import Grid
from value_iter import ValueIter
from q_learning import QLearning

small = """
___+
_#_-
____
"""

large = """
__________
_###__##__
_#+___##__
_#____##__
______##__
_#________
____-_____
__#####___
___-_+____
__________
"""

def validate_algs(grid, title):
    vi = ValueIter(grid)
    vi.iterate()
    vi.make_figure(title)

    ql = QLearning(grid)
    ql.iterate()
    ql.make_figure(title)

if __name__ == "__main__":
    grid = Grid.from_string(small)
    validate_algs(grid, "grid-small")
    grid = Grid.from_string(large)
    validate_algs(grid, "grid-large")
    grid = Grid.from_string(large, no_walls=True)
    validate_algs(grid, "grid-large-nowalls")

    for gamma in [1.0, 0.9, 0.1]:
        grid = Grid.from_string(large)
        grid.gamma = gamma
        validate_algs(grid, f"gamma-{gamma}")

    for no_reward in [0.0, -0.1, -0.3]:
        grid = Grid.from_string(large)
        grid.no_reward = no_reward
        grid.gamma = 0.25
        validate_algs(grid, f"noreward-{abs(no_reward)}")
    
    for ps in [[0.8, 0.15, 0.05], [0.5, 0.35, 0.15]]:
        grid = Grid.from_string(large)
        grid.p_perform = ps[0]
        grid.p_sidestep = ps[1]
        grid.p_backstep = ps[2]
        validate_algs(grid, f"ps-{ps[0]}-{ps[1]}-{ps[2]}")
