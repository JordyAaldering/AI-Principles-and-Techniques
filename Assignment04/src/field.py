from enum import Enum

class Field(Enum):
	EMPTY = '_'
	WALL = '#'
	REWARD = '+'
	NEG_REWARD = '-'

	def get_color(self):
		if self == Field.EMPTY:
			return 0.95, 0.95, 1.00, 1.0
		elif self == Field.WALL:
			return 0.05, 0.05, 0.10, 1.0
		elif self == Field.REWARD:
			return 0.20, 0.80, 0.25, 1.0
		else: # self == Field.NEG_REWARD
			return 0.80, 0.20, 0.25, 1.0

	def __str__(self):
		return self.value
