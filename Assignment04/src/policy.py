from mdp import Mdp

class Policy():
    def __init__(self, mdp: Mdp):
        self.grid = [row[:] for row in mdp.grid]
