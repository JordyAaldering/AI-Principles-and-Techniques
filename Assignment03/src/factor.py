import itertools

def get_permutations(size):
    permutations = set()
    for comb in itertools.combinations_with_replacement([True, False], size):
        for perm in itertools.permutations(comb):
            permutations.add(perm)
    return list(permutations)

class Factor():
    @staticmethod
    def make(bayes_net, var, factors, evidence):
        variables = factors[var]
        variables.sort()

        parents = [p for p in bayes_net.net[var]["parents"]]
        parents.append(var)

        asg = {}
        entries = {}
        for perm in get_permutations(len(parents)):
            violate = False
            for key, val in zip(parents, perm):
                if key in evidence and evidence[key] != val:
                    violate = True
                    break

                asg[key] = val
            
            if not violate:
                key = tuple(asg[v] for v in variables)
                prob = bayes_net.probability(var, asg)
                entries[key] = prob
        
        return variables, entries

    @staticmethod
    def pointwise(var, factor1, factor2):
        new_vars = []
        new_vars.extend(factor1[0])
        new_vars.extend(factor2[0])
        new_vars = list(set(new_vars))
        new_vars.sort()

        asg = {}
        table = {}
        for perm in get_permutations(len(new_vars)):
            for key, val in zip(new_vars, perm):
                asg[key] = val
            
            key = tuple(asg[v] for v in new_vars)
            key1 = tuple(asg[v] for v in factor1[0])
            key2 = tuple(asg[v] for v in factor2[0])
            prob = factor1[1][key1] * factor2[1][key2]
            table[key] = prob

        return new_vars, table

    @staticmethod
    def sumout(var, factors):
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
                result = Factor.pointwise(var, result, factor)

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
