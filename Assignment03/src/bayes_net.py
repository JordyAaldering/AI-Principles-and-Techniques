import itertools
import json

class BayesNet():
    def __init__(self, path):
        with open(path) as f:
            self.net = json.load(f)

    def sort_topological(self):
        variables = list(self.net.keys())
        variables.sort()
        
        vars_sorted = set()
        while len(vars_sorted) < len(variables):
            for v in variables:
                if all(parent in vars_sorted for parent in self.net[v]["parents"]):
                    vars_sorted.add(v)
        
        return list(vars_sorted)
    
    def probability(self, var, evidence):
        parents = self.net[var]["parents"]
        if len(parents) == 0:
            prob = self.net[var]["prob"]
        else:
            key = str([evidence[p] for p in parents])
            prob = self.net[var]["prob"][key]
        
        return prob if evidence[var] else 1 - prob
    
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

        asg = {}
        entries = {}
        for perm in self.get_permutations(len(parents)):
            violate = False
            for key, val in zip(parents, perm):
                if key in evidence and evidence[key] != val:
                    violate = True
                    break

                asg[key] = val
            
            if not violate:
                key = tuple(asg[v] for v in variables)
                prob = self.probability(var, asg)
                entries[key] = prob
        
        return variables, entries
    
    def factor_pointwise(self, var, factor1, factor2):
        new_vars = []
        new_vars.extend(factor1[0])
        new_vars.extend(factor2[0])
        new_vars = list(set(new_vars))
        new_vars.sort()

        asg = {}
        table = {}
        for perm in self.get_permutations(len(new_vars)):
            for key, val in zip(new_vars, perm):
                asg[key] = val
            
            key = tuple(asg[v] for v in new_vars)
            key1 = tuple(asg[v] for v in factor1[0])
            key2 = tuple(asg[v] for v in factor2[0])
            prob = factor1[1][key1] * factor2[1][key2]
            table[key] = prob

        return new_vars, table

    def factor_sumout(self, var, factors):
        indices = []
        pwfactors = []
        for i, factor in enumerate(factors):
            if var in factor[0]:
                pwfactors.append(factor)
                indices.append(i)
        
        if len(pwfactors) > 1:
            for i in reversed(indices):
                del factors[i]
            
            result = pwfactors[0]
            for factor in pwfactors[1:]:
                result = self.factor_pointwise(var, result, factor)

            factors.append(result)

        for i, factor in enumerate(factors):
            for j, v in enumerate(factor[0]):
                if v == var:
                    newvariables = factor[0][:j] + factor[0][j+1:]

                    newentries = {}
                    for entry in factor[1]:
                        entry = list(entry)
                        newkey = tuple(entry[:j] + entry[j+1:])

                        entry[j] = True
                        prob1 = factor[1][tuple(entry)]
                        entry[j] = False
                        prob2 = factor[1][tuple(entry)]
                        prob = prob1 + prob2
                        
                        newentries[newkey] = prob

                    factors[i] = (newvariables, newentries)
                    if len(newvariables) == 0:
                        del factors[i]
        
        return factors

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
        
        normalize = lambda dist: tuple(x * 1 / sum(dist) for x in dist)
        normalized = normalize((result[1][(False,)], result[1][(True,)]))
        return normalized
