from enum import Enum

class Action(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def get_dir(self, width: int):
        if self == Action.UP:
            return -width
        elif self == Action.RIGHT:
            return 1
        elif self == Action.DOWN:
            return width
        else: # self == Action.LEFT
            return -1

    def next_action(self):
        return Action((self.value + 1) % 4)

    def prev_action(self):
        return Action((self.value - 1) % 4)

    def back_action(self):
        return Action((self.value + 2) % 4)
    
    @staticmethod
    def as_list():
        return [Action.UP, Action.RIGHT, Action.DOWN, Action.LEFT]

    def __str__(self):
        if self == Action.UP:
            return "U"
        elif self == Action.RIGHT:
            return "R"
        elif self == Action.DOWN:
            return "D"
        elif self == Action.LEFT:
            return "L"
