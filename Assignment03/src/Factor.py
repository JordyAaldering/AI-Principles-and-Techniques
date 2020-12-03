import copy
import itertools

class Factor:

    @staticmethod
    def make_factors(var, network, evidence):
        variables = network.values[var]
        variables.sort()

        allvars = copy.deepcopy(network.parents[var])
        allvars.append(var)
        
        perms = Factor.gen_permutations(len(allvars))

        asg = {}
        entries = {}
        for perm in perms:
            violate = False
            for pair in zip(allvars, perm):
                if pair[0] in evidence and evidence[pair[0]] != pair[1]:
                    violate = True
                    break
                asg[pair[0]] = pair[1]

            if violate:
                continue

            key = tuple(asg[v] for v in variables)
            prob = self.query_given(var, asg)
            entries[key] = prob

        return (variables, entries)

    @staticmethod
    def gen_permutations(length):
        perms = set()
        for comb in itertools.combinations_with_replacement([False, True], length):
            for perm in itertools.permutations(comb):
                perms.add(perm)
        return list(perms)

    @staticmethod
    def point_wise(var, factor1, factor2):
        newvariables = []
        newvariables.extend(factor1[0])
        newvariables.extend(factor2[0])
        newvariables = list(set(newvariables))
        newvariables.sort()

        perms = Factor.gen_permutations(len(newvariables))

        asg = {}
        newtable = {}
        for perm in perms:
            for pair in zip(newvariables, perm):
                asg[pair[0]] = pair[1]
            key = tuple(asg[v] for v in newvariables)
            key1 = tuple(asg[v] for v in factor1[0])
            key2 = tuple(asg[v] for v in factor2[0])
            prob = factor1[1][key1] * factor2[1][key2]
            newtable[key] = prob

        return (newvariables, newtable)

    @staticmethod
    def sum_out(var, factors):
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
                result = Factor.point_wise(var, result, factor)

            factors.append(result)

        for i, factor in enumerate(factors):
            for j, v in enumerate(factor[0]):
                if v != var:
                    continue

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
