from field import Field
from action import Action
import numpy as np

'''
Value iteration
1) Initialize Q0 to 0
    - Q(a,s): The expected value of doing action a in state s
2) Initialize V0 to 0
    - V(s): (utility) The expected sum of rewards
3) Update Q values for all states and actions
4) Compute the new value function for all states
5) If not converged; set k += 1 and go to (3)
6) Policy pi*(s) = argmax_a Q(s,a)
'''

class ValueIter():
    p_perform = 0.7
    p_sidestep = 0.2
    p_backstep = 0.1

    pos_reward = 1.0
    neg_reward = -1.0
    no_reward = -0.04

    def __init__(self, width, height, grid: [Field]):
        self.width = width
        self.height = height
        size = width * height

        self.grid = grid
        self.state_space = list(range(size))

        self.Q = {}
        self.V = [0] * size
        self.policy = np.full(size, Action.UP)

        for state in self.state_space:
            for action in Action.as_list():
                new_state = state + action.get_dir(width)
                reward = self.no_reward

                if not self.move_is_valid(state, new_state):
                    new_state = state # revert to the previous state
                elif self.grid[new_state] == Field.REWARD:
                    reward = self.pos_reward
                elif self.grid[new_state] == Field.NEG_REWARD:
                    reward = self.neg_reward
                
                self.Q[(state, action)] = (new_state, reward)

    def iterate(self, gamma):
        converged = False
        while not converged:
            delta = 0
            for state in self.state_space:
                if self.is_end_state(state):
                    self.V[state] = 0
                    continue
                
                old_v = self.V[state]
                new_v = [0, 0, 0, 0]

                for i, action in enumerate(Action.as_list()):
                    new_state, reward = self.Q.get((state, action))
                    new_v[i] += self.p_perform * (reward + gamma * self.V[new_state])

                    new_state, reward = self.Q.get((state, action.next_action()))
                    new_v[i] += self.p_sidestep / 2 * (reward + gamma * self.V[new_state])

                    new_state, reward = self.Q.get((state, action.prev_action()))
                    new_v[i] += self.p_sidestep / 2 * (reward + gamma * self.V[new_state])

                    new_state, reward = self.Q.get((state, action.back_action()))
                    new_v[i] += self.p_backstep * (reward + gamma * self.V[new_state])
                
                self.V[state] = max(new_v)
                delta = max(delta, np.abs(old_v - self.V[state]))
                converged = delta < 1e-10

        for state in self.state_space:
            new_vs = [0, 0, 0, 0]
            for i, action in enumerate(Action.as_list()):
                new_state, reward = self.Q.get((state, action))
                new_vs[i] = reward + gamma * self.V[new_state]
            
            new_vs = np.array(new_vs)
            best_action_idx = np.where(new_vs == new_vs.max())[0][0]
            self.policy[state] = Action(best_action_idx)

    def move_is_valid(self, state, new_state):
        return (new_state in self.state_space and
            # check if a horizontal move ended up in a new row
            not (state % self.width == 0 and new_state % self.width == self.width - 1) and
            not (state % self.width == self.width - 1 and new_state % self.width == 0))
    
    def is_end_state(self, state):
        field = self.grid[state]
        return field == Field.REWARD or field == Field.NEG_REWARD or field == Field.WALL
    
    def __str__(self):
        s = ""
        for i, field in enumerate(self.grid):
            if field == field.EMPTY:
                s += str(self.policy[i])
            else:
                s += str(field)
            if i % self.width == self.width - 1:
                s += "\n"
        return s