from field import Field

import random

class Grid():
    p_perform = 0.7
    p_sidestep = 0.2
    p_backstep = 0.1
    
    gamma = 0.75

    pos_reward = 1.0
    neg_reward = -1.0
    no_reward = -0.04

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [Field.EMPTY] * self.size

        self.reset_pos()
    
    @classmethod
    def from_string(cls, s, no_walls=False):
        lines = s.split("\n")
        lines = list(filter(None, lines))

        width = len(lines[0])
        height = len(lines)
        grid = cls(width, height)

        i = 0
        for row in lines:
            for c in row:
                field = Field(c)
                if no_walls and field == Field.WALL:
                    field = field.EMPTY
                grid.grid[i] = field
                i += 1
        
        return grid

    def reset_pos(self):
        self.pos = random.randrange(0, self.size)

    @property
    def size(self):
        return self.width * self.height

    def get_reward(self):
        field = self.grid[self.pos]
        if field == Field.REWARD:
            return self.pos_reward
        elif field == Field.NEG_REWARD:
            return self.neg_reward
        else:
            return self.no_reward

    def try_step(self, action):
        p = random.uniform(0.0, 1.0)
        if p < self.p_perform:
            pass # action = action
        elif p < self.p_perform + self.p_sidestep / 2:
            action = action.next_action()
        elif p < self.p_perform + self.p_sidestep:
            action = action.prev_action()
        else: # p < self.p_perform + self.p_sidestep + self.backstep
            action = action.back_action()

        return self.make_step(action)

    def make_step(self, action):
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

    def is_end_state(self, pos):
        field = self.grid[pos]
        return field == Field.REWARD or field == Field.NEG_REWARD
