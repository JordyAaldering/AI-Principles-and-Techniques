from util import get_permutations
from factor import Factor
import json

class BayesNet():
    def __init__(self, path):
        with open(path) as f:
            self.net = json.load(f)

    def probability(self, var, evidence):
        parents = self.net[var]["parents"]
        key = str([evidence[p] for p in parents])
        prob = self.net[var]["prob"][key]
        return prob if evidence[var] else 1 - prob
    
    def eliminate(self, var, evidence):
        eliminated = set()
        factors = []

        while len(eliminated) < len(self.net):
            variables = [v for v in list(self.net.keys()) if v not in eliminated]
            variables = [v for v in variables if all(c in eliminated for c in self.net[v]["children"])]

            factor_vars = {}
            for v in variables:
                factor_vars[v] = [p for p in self.net[v]["parents"] if p not in evidence]
                if v not in evidence:
                    factor_vars[v].append(v)
            
            v = sorted(factor_vars.keys(), key=(lambda x: (len(factor_vars[x]), x)))[0]
            if len(factor_vars[v]) > 0:
                factors.append(Factor.make(self, v, factor_vars, evidence))
            
            if v != var and v not in evidence:
                factors = Factor.sumout(v, factors)

            eliminated.add(v)

        result = factors[0]
        for f in factors[1:]:
            result = Factor.pointwise(var, result, f)
        
        dist = result[1][(False,)], result[1][(True,)]
        return tuple(x * 1 / sum(dist) for x in dist)
