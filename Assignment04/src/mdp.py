import random
from action import Action
from field import Field

class MDP():
    deterministic = True
    p_perform = 0.7
    p_sidestep = 0.2
    p_backstep = 0.1
    p_no_step = 0.0

    pos_reward = 1.0
    neg_reward = -1.0
    no_reward = -0.04

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.restart()

    def restart(self):
        self.grid = [[Field.EMPTY for i in range(self.height)]
            for j in range(self.width)]
        
        self.x_pos = 0
        self.y_pos = 0
        self.terminated = False
        self.actions_counter = 0

    def try_action(self, action: Action) -> float:
        p = random.randrange(1.0)
        if self.deterministic or p < self.p_perform:
            pass # action = action
        elif p < self.p_perform + self.p_sidestep / 2:
            action = action.next_action()
        elif p < self.p_perform + self.p_sidestep:
            action = action.prev_action()
        elif p < self.p_perform + self.p_sidestep + self.p_backstep:
            action = action.back_action()
        
        self.do_action(action)
        self.actions_counter += 1
        return self.get_reward()
    
    def do_action(self, action: Action):
        if self.action_is_valid(action):
            x, y = action.get_dir()
            self.x_pos += x
            self.y_pos += y

    def action_is_valid(self, action: Action) -> bool:
        x, y = action.get_dir()
        x += self.x_pos
        y += self.y_pos
        return (0 <= x < self.width and 0 <= y < self.height
            and self.grid[x][y] != Field.OBSTACLE)

    def get_reward(self) -> float:
        field = self.grid[self.x_pos][self.y_pos]
        if field == Field.EMPTY:
            return self.no_reward
        elif field == Field.REWARD:
            self.terminated = True
            return self.pos_reward
        elif field == Field.NEG_REWARD:
            self.terminated = True
            return self.neg_reward
    
    def __str__(self) -> str:
        return "\n".join(
            ["".join([x.value for x in row])
                for row in self.grid])
