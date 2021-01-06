def pi(self, cell, action):
    '''
    Determines the probability of executing an action in a cell.
    '''
    if len(self.policy) == 0:
        return 1 # value iteration

    if self.policyActionForCell(cell) == action:
        return 1 # policy allows this action
    else:
        return 0 # policy forbids this action
