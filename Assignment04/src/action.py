from enum import Enum

class Action(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def get_dir(self):
        if self == Action.UP:
            return (0, 1)
        elif self == Action.RIGHT:
            return (1, 0)
        elif self == Action.DOWN:
            return (0, -1)
        elif self == Action.LEFT:
            return (-1, 0)

    def next_action(self):
        return Action((self.value + 1) % 4)

    def prev_action(self):
        return Action((self.value - 1) % 4)

    def back_action(self):
        return Action((self.value + 2) % 4)
