from field import Field
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

if __name__ == "__main__":
    grid_small = Grid.from_string(small)
    grid_large = Grid.from_string(large)

    vi = ValueIter(grid_large)
    vi.iterate()
    vi.show_figure()

    ql = QLearning(grid_large)
    ql.play()
    ql.show_figure()
