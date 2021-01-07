from enum import Enum

class Field(Enum):
	EMPTY = '_'
	WALL = '#'
	REWARD = '+'
	NEG_REWARD = '-'

	def __str__(self):
		return self.value