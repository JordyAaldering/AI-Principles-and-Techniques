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
        
        vars_sorted = []
        while len(vars_sorted) < len(variables):
            for v in variables:
                if v in vars_sorted:
                    continue
                if all(parent in vars_sorted for parent in self.net[v]["parents"]):
                    vars_sorted.append(v)
        
        print("Variables topologically sorted:", vars_sorted)
        return vars_sorted
    
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
        permutations = []
        for comb in itertools.combinations_with_replacement([True, False], size):
            for perm in itertools.permutations(comb):
                if perm not in permutations:
                    permutations.append(perm)
        return permutations

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
