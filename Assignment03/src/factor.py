from copy import deepcopy
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
        '''
        Makes a new factor containing:
            a list of variables
            a dictionary mapping from possible states
                to their corresponding probabilities
        '''
        variables = sorted(factors[var])
        parents = deepcopy(bayes_net.net[var]["parents"]) + [var]

        asg = {}
        entries = {}
        for perm in get_permutations(len(parents)):
            for key, val in zip(parents, perm):
                if key in evidence and evidence[key] != val:
                    break

                asg[key] = val
            
            else: # the inner for loop has not been broken
                key = tuple(asg[v] for v in variables)
                prob = bayes_net.probability(var, asg)
                entries[key] = prob
        
        return variables, entries

    @staticmethod
    def pointwise(var, factor1, factor2):
        new_vars = set(factor1[0])
        new_vars.update(factor2[0])

        asg = {}
        table = {}
        for perm in get_permutations(len(new_vars)):
            for key, val in zip(new_vars, perm):
                asg[key] = val
            
            key1 = tuple(asg[v] for v in factor1[0])
            key2 = tuple(asg[v] for v in factor2[0])
            prob = factor1[1][key1] * factor2[1][key2]
            
            key = tuple(asg[v] for v in new_vars)
            table[key] = prob

        return new_vars, table

    @staticmethod
    def sumout(var, factors):
        var_factors = []
        indices = []

        for i, factor in enumerate(factors):
            if var in factor[0]:
                var_factors.append(factor)
                indices.append(i)
        
        if len(var_factors) > 1:
            for i in reversed(indices):
                del factors[i]
            
            result = var_factors[0]
            for factor in var_factors[1:]:
                result = Factor.pointwise(var, result, factor)

            factors.append(result)

        for i, factor in enumerate(factors):
            # enumerate over all hidden variables of the factor
            for j, v in enumerate(factor[0]):
                if v == var:
                    new_variables = factor[0][:j] + factor[0][j+1:]
                    new_entries = {}

                    for entry in factor[1]:
                        entry = list(entry)
                        new_key = tuple(entry[:j] + entry[j+1:])

                        entry[j] = True
                        prob1 = factor[1][tuple(entry)]
                        entry[j] = False
                        prob2 = factor[1][tuple(entry)]
                        prob = prob1 + prob2
                        
                        new_entries[new_key] = prob

                    # replace the old factor
                    factors[i] = (new_variables, new_entries)
                    if len(new_variables) == 0:
                        del factors[i]
        
        return factors
