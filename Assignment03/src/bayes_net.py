from factor import Factor
import json

class BayesNet():
    def __init__(self, path):
        with open(path) as f:
            self.net = json.load(f)

    def probability(self, query, evidence):
        parents = self.net[query]["parents"]
        key = str([evidence[p] for p in parents])
        prob = self.net[query]["prob"][key]
        return prob if evidence[query] else 1 - prob
    
    def eliminate(self, query, evidence):
        eliminated = set()
        factors = []

        while len(eliminated) < len(self.net):
            variables = [v for v in list(self.net.keys()) if v not in eliminated and
                all(c in eliminated for c in self.net[v]["children"])]

            factor_vars = {}
            for v in variables:
                factor_vars[v] = [p for p in self.net[v]["parents"] + [v] if p not in evidence]
            
            var = sorted(factor_vars.keys(), key=(lambda x: (len(factor_vars[x]), x)))[0]
            if len(factor_vars[var]) > 0:
                factors.append(Factor.make(self, var, factor_vars, evidence))
            
            if var != query:
                factors = Factor.sumout(var, factors)

            eliminated.add(var)

        result = factors[0]
        for f in factors[1:]:
            result = Factor.pointwise(query, result, f)
        
        dist = result[1][(False,)], result[1][(True,)]
        return tuple(x * 1 / sum(dist) for x in dist)
