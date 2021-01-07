from action import Action
from grid import GridWorld
import numpy as np

class QLearning():
    epsilon = 0.1
    alpha = 0.75
    gamma = 0.75

    def __init__(self, grid: GridWorld):
        self.env = grid
        self.q_table = dict()

        for i in range(grid.width * grid.height):
            self.q_table[i] = {
                Action.UP: 0,
                Action.RIGHT: 0,
                Action.DOWN: 0,
                Action.LEFT: 0,
            }
    
    def choose_action(self, available_actions):
        if np.random.uniform(0, 1) < self.epsilon:
            i = np.random.randint(0, len(available_actions))
            action = available_actions[i]
        else:
            q_vals_of_state = self.q_table[self.env.pos]
            max_val = max(q_vals_of_state.values())
            action = np.random.choice([k for k, v in q_vals_of_state.items() if v == max_val])
        
        return action
    
    def learn(self, old_state, reward, new_state, action):
        q_vals_of_state = self.q_table[new_state]
        max_q_val = max(q_vals_of_state.values())
        old_q_val = self.q_table[old_state][action]

        self.q_table[old_state][action] = (1 - self.alpha) * old_q_val + self.alpha * (reward + self.gamma * max_q_val)

    def play(self, trials = 500, max_steps = 1000):
        for trial in range(trials):
            total_reward = 0
            step = 0
            game_over = False
            
            while step < max_steps and not game_over:
                old_state = self.env.pos
                action = self.choose_action(Action.as_list())
                reward = self.env.make_step(action)
                new_state = self.env.pos

                self.learn(old_state, reward, new_state, action)
                total_reward += reward
                step += 1

                if self.env.is_end_state(new_state):
                    self.env = GridWorld(self.env.width, self.env.height, self.env.grid)
                    game_over = True

    def __str__(self):
        s = ""
        for i in range(self.env.width * self.env.height):
            field = self.env.grid[i]
            if field == field.EMPTY:
                actions = self.q_table[i]
                action = max(actions, key=actions.get)
                s += str(action)
            else:
                s += str(field)
            if i % self.env.width == self.env.width - 1:
                s += "\n"
        return s
