from Factor import Factor

class VariableElim:

    def __init__(self, network):
        """
        Initialize the variable elimination algorithm with the specified network.
        Add more initializations if necessary.
        """
        self.network = network

    def run(self, query, evidence, elim_order):
        """
        Use the variable elimination algorithm to find out the probability
        distribution of the query variable given the observed variables

        Input:
            query:      The query variable
            evidence:   A dictionary of the observed variables {variable: value}
            elim_order: Either a list specifying the elimination ordering
                        or a function that will determine an elimination ordering
                        given the network during the run

        Output: A variable holding the probability distribution
                for the query variable
        """
        eliminated = []
        factors = []

        while len(eliminated) < len(self.network.nodes):
            var = elim_order[0]
            factors.append(Factor.make_factors(var, self.network, evidence))

            if var != query and var not in evidence:
                factors = Factor.sum_out(var, factors)

            eliminated.append(var)
            
        if len(factors) >= 2:
            result = factors[0]
            for factor in factors[1:]:
                result = Factor.point_wise(var, result, factor)
        else:
            result = factors[0]

        return result
