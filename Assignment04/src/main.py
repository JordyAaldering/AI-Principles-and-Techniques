from action import Action
from field import Field
from mdp import MDP

if __name__ == "__main__":
    mdp = MDP(10, 10)
    for i in range(15):
        mdp.try_action(Action.UP)
        mdp.try_action(Action.UP)
        mdp.try_action(Action.RIGHT)
        mdp.try_action(Action.RIGHT)
        mdp.try_action(Action.RIGHT)
        mdp.restart()
    print(mdp)
    
    mdp = MDP(10, 10)
    mdp.grid[5][5] = Field.REWARD
    for i in range(100):
        mdp.try_action(Action.UP)
        mdp.try_action(Action.RIGHT)
        mdp.try_action(Action.DOWN)
        mdp.try_action(Action.LEFT)
