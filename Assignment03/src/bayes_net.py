from factor import Factor
import json

class BayesNet():
    def __init__(self, path):
        '''
        Initializes the network represented as a dictionary.
        This dictionary maps variable names to:
            a list of its parents
            a list of its children
            a dictionary containing possible value assignments
                and their corresponding probabilities
        '''
        with open(path) as f:
            self.net = json.load(f)

    def probability(self, query, evidence):
        '''
        Returns the probability that the query variable is true,
        given the evidence set containing variables and their values.
        This is the same as P(query | evidence).
        '''
        parents = self.net[query]["parents"]
        key = str([evidence[p] for p in parents])
        prob = self.net[query]["prob"][key]
        return prob if evidence[query] else 1 - prob
    
    def eliminate(self, query, evidence):
        '''
        Returns the distribution over the query variable using variable elimination,
        given the evidence set containing variables and their values.
        '''
        eliminated = set()
        factors = []

        while len(eliminated) < len(self.net):
            # filter variables that have been eliminated
            # or whose children have been eliminated
            variables = [v for v in list(self.net.keys()) if v not in eliminated and
                all(c in eliminated for c in self.net[v]["children"])]

            factor_vars = {}
            for v in variables:
                factor_vars[v] = [p for p in self.net[v]["parents"] + [v] if p not in evidence]
            
            # sort depending on number of variables in each factor
            var = sorted(factor_vars.keys(), key=(lambda x: (len(factor_vars[x]), x)))[0]
            
            if len(factor_vars[var]) > 0:
                factors.append(Factor.make(self, var, factor_vars, evidence))
            
            # if the variable is hidden then sum it out
            if var != query:
                factors = Factor.sumout(var, factors)

            eliminated.add(var)

        # calculate pointwise product
        result = factors[0]
        for f in factors[1:]:
            result = Factor.pointwise(query, result, f)
        
        # normalize result
        dist = result[1][(False,)], result[1][(True,)]
        return tuple(x * 1 / sum(dist) for x in dist)
