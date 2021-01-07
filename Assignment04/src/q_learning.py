from action import Action
from grid import Grid
import numpy as np
import random

class QLearning():
    epsilon = 0.1
    alpha = 0.75
    gamma = 0.75

    def __init__(self, grid: Grid):
        self.grid = grid
        self.q_table = dict()

        for i in range(grid.width * grid.height):
            self.q_table[i] = {
                Action.UP: 0,
                Action.RIGHT: 0,
                Action.DOWN: 0,
                Action.LEFT: 0,
            }
    
    def choose_action(self):
        if random.uniform(0, 1) < self.epsilon:
            i = random.randrange(0, 4)
            return Action.as_list()[i]
        else:
            actions = self.q_table[self.grid.pos]
            return max(actions, key=actions.get)
    
    def learn(self, old_state, action, new_state, reward):
        old_q_val = self.q_table[old_state][action]
        new_q_vals = self.q_table[new_state]
        max_q_val = max(new_q_vals.values())

        self.q_table[old_state][action] = ((1 - self.alpha) * old_q_val
            + self.alpha * (reward + self.gamma * max_q_val))

    def play(self, trials = 500, max_steps = 1000):
        for _trial in range(trials):
            total_reward = 0

            for _step in range(max_steps):
                old_state = self.grid.pos
                action = self.choose_action()
                reward = self.grid.make_step(action)
                new_state = self.grid.pos

                self.learn(old_state, action, new_state, reward)
                total_reward += reward

                if self.grid.is_end_state(new_state):
                    self.grid.reset()
                    break

    def __str__(self):
        s = ""
        for i in range(self.grid.width * self.grid.height):
            field = self.grid.grid[i]
            if field == field.EMPTY:
                actions = self.q_table[i]
                action = max(actions, key=actions.get)
                s += str(action)
            else:
                s += str(field)
            if i % self.grid.width == self.grid.width - 1:
                s += "\n"
        return s
