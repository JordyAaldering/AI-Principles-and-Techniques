from action import Action
from field import Field
import random

class GridWorld():
    pos_reward = 1.0
    neg_reward = -1.0
    no_reward = -0.04

    def __init__(self, width, height, grid: [Field]):
        self.width = width
        self.height = height
        self.grid = grid

        self.pos = random.randint(0, width * height - 1)
    
    def get_reward(self):
        field = self.grid[self.pos]
        if field == Field.REWARD:
            return self.pos_reward
        elif field == Field.NEG_REWARD:
            return self.neg_reward
        else:
            return self.no_reward

    def make_step(self, action: Action):
        new_pos = self.pos + action.get_dir(self.width)
        reward = self.no_reward

        if self.move_is_valid(self.pos, new_pos):
            self.pos = new_pos
            if self.grid[new_pos] == Field.REWARD:
                reward = self.pos_reward
            elif self.grid[new_pos] == Field.NEG_REWARD:
                reward = self.neg_reward
        
        return reward
    
    def move_is_valid(self, pos, new_pos):
        return (0 <= new_pos < self.width * self.height and
            self.grid[new_pos] != Field.WALL and
            # check if a horizontal move ended up in a new row
            not (pos % self.width == 0 and new_pos % self.width == self.width - 1) and
            not (pos % self.width == self.width - 1 and new_pos % self.width == 0))

    def is_end_state(self, state):
        field = self.grid[state]
        return field == Field.REWARD or field == Field.NEG_REWARD
