from field import Field
from grid import GridWorld
from value_iter import ValueIter
from q_learning import QLearning

if __name__ == "__main__":
    width, height = (5, 4)
    grid = [Field.EMPTY] * width * height
    grid[7] = Field.WALL
    grid[10] = Field.NEG_REWARD
    grid[13] = Field.WALL
    grid[14] = Field.WALL
    grid[15] = Field.WALL
    grid[19] = Field.REWARD

    vi = ValueIter(width, height, grid)
    vi.iterate(0.8)
    print(vi)

    env = GridWorld(width, height, grid)
    ql = QLearning(env)
    ql.play()

    print(ql)
