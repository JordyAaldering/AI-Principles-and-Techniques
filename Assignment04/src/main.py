from field import Field
from grid import Grid
from value_iter import ValueIter
from q_learning import QLearning

if __name__ == "__main__":
    width, height = (5, 4)
    grid = Grid(width, height)
    grid.grid[7] = Field.WALL
    grid.grid[10] = Field.NEG_REWARD
    grid.grid[13] = Field.WALL
    grid.grid[14] = Field.WALL
    grid.grid[15] = Field.WALL
    grid.grid[19] = Field.REWARD

    vi = ValueIter(grid)
    vi.iterate()
    vi.show_figure()

    ql = QLearning(grid)
    ql.play()
    ql.show_figure()
