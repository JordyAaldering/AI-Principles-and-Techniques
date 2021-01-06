from mdp import MDP

'''
Value iteration
1) Initialize Q0 to 0
    - Q(a,s): The expected value of doing action a in state s
2) Initialize V0 to 0
    - V(s): (utility) The expected sum of rewards
3) Update Q values for all states and actions
4) Compute the new value function for all states
5) If not converged; set k += 1 and go to (3)
6) Policy pi*(s) = argmax_a Q(s,a)
'''

class ValueIter():
    def __init__(self, mdp: MDP):
        self.Q = [[0 for i in range(mdp.width)] for j in range(mdp.height)]
        self.V = [[0 for i in range(mdp.width)] for j in range(mdp.height)]

    def iterate(self):
        k = 0
        converged = False

        while not converged:
            k += 1
            break
