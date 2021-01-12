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
    
    def probability(self, variable, evidence):
        parents = self.net[variable]["parents"]
        if len(parents) == 0:
            prob = self.net[variable][prob]
        else:
            key = str([evidence[p] for p in parents])
            prob = self.net[variable]["prob"][key]
        
        prob = prob if evidence[variable] else 1 - prob
        print(f"Variable {variable} with evidence {evidence} has probability: {prob}")
        return prob
