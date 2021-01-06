from mdp import MDP
from policy import Policy

if __name__ == "__main__":
    mdp = MDP(10, 5)
    policy = Policy(mdp)

    print("MDP:\n", mdp)