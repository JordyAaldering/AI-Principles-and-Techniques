import itertools
import json

class BayesNet():
    def __init__(self, path):
        with open(path) as f:
            self.net = json.load(f)

        print("Bayes network succesfully loaded:", self.net)

    def sort_topological(self):
        variables = list(self.net.keys())
        variables.sort()
        
        vars_sorted = set()
        while len(vars_sorted) < len(variables):
            for v in variables:
                if all(parent in vars_sorted for parent in self.net[v]["parents"]):
                    vars_sorted.add(v)
        
        print("Variables topologically sorted:", list(vars_sorted))
        return list(vars_sorted)
    
    def probability(self, var, evidence):
        parents = self.net[var]["parents"]
        if len(parents) == 0:
            prob = self.net[var][prob]
        else:
            key = str([evidence[p] for p in parents])
            prob = self.net[var]["prob"][key]
        
        prob = prob if evidence[var] else 1 - prob
        print(f"Variable {var} with evidence {evidence} has probability: {prob}")
        return prob
    
    def get_permutations(self, size):
        permutations = set()
        for comb in itertools.combinations_with_replacement([True, False], size):
            for perm in itertools.permutations(comb):
                permutations.add(perm)
        return list(permutations)

    def make_factor(self, var, factors, evidence):
        variables = factors[var]
        variables.sort()

        parents = [p for p in self.net[var]["parents"]]
        parents.append(var)

        permutations = self.get_permutations(len(parents))

        asg = {}
        entries = {}
        for perm in permutations:
            violate = False
            for key, val in zip(parents, perm):
                if key in evidence and evidence[key] != val:
                    violate = True
                    break

                asg[key] = val
            
            if violate:
                continue

            key = tuple(asg[v] for v in variables)
            prob = self.probability(var, asg)
            entries[key] = prob
        
        return variables, entries
    
    def factor_pointwise(self, var, factor1, factor2):
        pass

    def factor_sumout(self, var, factors):
        pass

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
                factors.append(self.make_factor(v, factor_vars, evidence))
            
            if v != var and v not in evidence:
                factors = self.factor_sumout(v, factors)

            eliminated.add(v)

        result = factors[0]
        if len(factors) >= 2:
            for f in factors[1:]:
                result = self.factor_pointwise(var, result, f)
        return result
