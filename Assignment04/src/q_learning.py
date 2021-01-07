from action import Action
from field import Field
from grid import Grid

import matplotlib.pyplot as plt
import numpy as np
import random

class QLearning():
    epsilon = 0.1
    alpha = 0.75
    gamma = 0.75

    def __init__(self, grid):
        self.grid = grid
        
        self.q_table = {}
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

    def play(self, trials=500, max_steps=1000):
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
                    self.grid.reset_pos()
                    break

    def show_figure(self, save=True, show=False):
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
                    actions = self.q_table[i]
                    action = max(actions, key=actions.get)
                    s = f"{action}\n{actions[action]:.2f}"
                    plt.text(x, y, s, ha="center", va="center")
        
        if save:
            plt.savefig("images/q_learning.png", bbox_inches="tight")
        if show:
            plt.show()

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
