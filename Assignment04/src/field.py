from enum import Enum

class Field(Enum):
	EMPTY = '_'
	OBSTACLE = '#'
	REWARD = '+'
	NEG_REWARD = '-'
