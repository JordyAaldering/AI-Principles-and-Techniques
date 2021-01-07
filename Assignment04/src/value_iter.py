from action import Action
from field import Field
from grid import Grid

import numpy as np

class ValueIter():
    gamma = 0.75
    delta = 1e-10

    p_perform = 0.7
    p_sidestep = 0.2
    p_backstep = 0.1

    def __init__(self, grid: Grid):
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
                    new_vs[i] += self.p_perform * (reward + self.gamma * self.V[new_state])

                    new_state, reward = self.Q.get((state, action.next_action()))
                    new_vs[i] += self.p_sidestep / 2 * (reward + self.gamma * self.V[new_state])

                    new_state, reward = self.Q.get((state, action.prev_action()))
                    new_vs[i] += self.p_sidestep / 2 * (reward + self.gamma * self.V[new_state])

                    new_state, reward = self.Q.get((state, action.back_action()))
                    new_vs[i] += self.p_backstep * (reward + self.gamma * self.V[new_state])
                
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

    def __str__(self):
        s = ""
        for i, field in enumerate(self.grid.grid):
            s += str(self.policy[i] if field == Field.EMPTY else field)
            if i % self.grid.width == self.grid.width - 1:
                s += "\n"
        return s
