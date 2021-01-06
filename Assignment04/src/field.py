from enum import Enum

class Field(Enum):
	EMPTY = ' '
	OBSTACLE = '#'
	REWARD = '+'
	NEG_REWARD = '-'
