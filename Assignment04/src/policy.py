from mdp import MDP
import numpy as np

class Policy():
    def __init__(self, mdp: MDP):
        self.grid = [[-np.inf for i in range(mdp.width)]
            for j in range(mdp.height)]
