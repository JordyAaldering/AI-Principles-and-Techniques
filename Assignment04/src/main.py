from grid import Grid
from field import Field
from value_iter import ValueIter

if __name__ == "__main__":
    grid = Grid(5, 4)
    grid.values[7] = Field.WALL
    grid.values[10] = Field.NEG_REWARD
    grid.values[13] = Field.WALL
    grid.values[14] = Field.WALL
    grid.values[15] = Field.WALL
    grid.values[19] = Field.REWARD

    vi = ValueIter(grid)
    vi.iterate(0.8)
    print(vi)
