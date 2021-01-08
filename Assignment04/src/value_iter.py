from action import Action
from field import Field

import matplotlib.pyplot as plt
import numpy as np

class ValueIter():
    gamma = 0.75
    delta = 1e-10

    def __init__(self, grid):
        self.grid = grid
        self.state_space = list(range(grid.size))

        self.Q = {}
        self.V = [0] * grid.size
        self.policy = np.full(grid.size, Action.UP)

        for state in self.state_space:
            for action in Action.as_list():
                self.grid.pos = state
                reward = self.grid.make_step(action)
                self.Q[(state, action)] = (self.grid.pos, reward)

    def iterate(self):
        converged = False
        while not converged:
            max_delta = 0
            for state in self.state_space:
                if self.grid.is_end_state(state):
                    self.V[state] = 0
                    continue
                
                old_v = self.V[state]
                new_vs = [0, 0, 0, 0]

                for i, action in enumerate(Action.as_list()):
                    new_state, reward = self.Q.get((state, action))
                    new_vs[i] += self.grid.p_perform * (reward + self.gamma * self.V[new_state])

                    new_state, reward = self.Q.get((state, action.next_action()))
                    new_vs[i] += self.grid.p_sidestep / 2 * (reward + self.gamma * self.V[new_state])

                    new_state, reward = self.Q.get((state, action.prev_action()))
                    new_vs[i] += self.grid.p_sidestep / 2 * (reward + self.gamma * self.V[new_state])

                    new_state, reward = self.Q.get((state, action.back_action()))
                    new_vs[i] += self.grid.p_backstep * (reward + self.gamma * self.V[new_state])
                
                self.V[state] = max(new_vs)
                max_delta = max(max_delta, np.abs(old_v - self.V[state]))
                converged = max_delta < self.delta

        for state in self.state_space:
            new_vs = [0, 0, 0, 0]
            for i, action in enumerate(Action.as_list()):
                new_state, reward = self.Q.get((state, action))
                new_vs[i] = reward + self.gamma * self.V[new_state]
            
            i = new_vs.index(max(new_vs))
            self.policy[state] = Action(i)

    def make_figure(self, title, save=True, show=False):
        colors = np.empty((self.grid.height, self.grid.width, 4))
        for i, field in enumerate(self.grid.grid):
            i = np.unravel_index(i, (self.grid.height, self.grid.width))
            colors[i] = field.get_color()
        
        plt.figure(figsize=(9,6))
        plt.imshow(colors)
        plt.axis("off")

        for y in range(self.grid.height):
            for x in range(self.grid.width):
                i = x + y * self.grid.width
                field = self.grid.grid[i]

                if field != Field.WALL and field != Field.REWARD and field != Field.NEG_REWARD:
                    s = f"{self.policy[i]}\n{self.V[i]:.2f}"
                    plt.text(x, y, s, ha="center", va="center")
        
        if save:
            plt.savefig(f"images/value_iter/{title}.png", bbox_inches="tight")
        if show:
            plt.show()

    def __str__(self):
        s = ""
        for i, field in enumerate(self.grid.grid):
            s += str(self.policy[i] if field == Field.EMPTY else field)
            if i % self.grid.width == self.grid.width - 1:
                s += "\n"
        return s
