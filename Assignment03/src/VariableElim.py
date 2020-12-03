class VariableElim:

    def __init__(self, network):
        """
        Initialize the variable elimination algorithm with the specified network.
        Add more initializations if necessary.
        """
        self.network = network

    def run(self, query, observed, elim_order):
        """
        Use the variable elimination algorithm to find out the probability
        distribution of the query variable given the observed variables

        Input:
            query:      The query variable
            observed:   A dictionary of the observed variables {variable: value}
            elim_order: Either a list specifying the elimination ordering
                        or a function that will determine an elimination ordering
                        given the network during the run

        Output: A variable holding the probability distribution
                for the query variable
        """
        eliminated = set()
        factors = []

        while len(eliminated) < len(self.network.nodes):
            variables = filter(lambda v: v not in eliminated, self.network.nodes)
            variables = filter(lambda v: all(c in eliminated for c in self.network.parents[v]), variables)

            factorvars = {}
            for v in variables:
                factorvars[v] = [p for p in self.network.parents[v] if p not in e]
                if v not in e:
                    factorvars[v].append(v)

            var = sorted(factorvars.keys(), key=(lambda x: (len(factorvars[x]), x)))[0]
            if len(factorvars[var]) > 0:
                factors.append(self.make_factor(var, factorvars, e))

            if var != query and var not in e:
                factors = self.sum_out(var, factors)

            eliminated.add(var)
            for factor in factors:
                asg = {}
                perms = list(self.gen_permutations(len(factors[0])))
                perms.sort()

                for perm in perms:
                    for pair in zip(factor[0], perm):
                        asg[pair[0]] = pair[1]
                    key = tuple(asg[v] for v in factor[0])

            if len(factors) >= 2:
                result = factors[0]
                for factor in factors[1:]:
                    result = self.point_wise(var, result, factor)
            else:
                result = factors[0]

            return result
