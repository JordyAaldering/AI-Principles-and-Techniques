import pandas as pd

class BayesNet:
    values = {}
    probabilities = {}
    parents = {}

    def __init__(self, filename):
        with open(filename, 'r') as file:
            line_number = 0
            for line in file:
                if line.startswith('network'):
                    self.name = ' '.join(line.split()[1:-1])
                elif line.startswith('variable'):
                    self.parse_variable(line_number, filename)
                elif line.startswith('probability'):
                    self.parse_probability(line_number, filename)
                line_number += 1

    def parse_probability(self, line_number, filename):
        line = open(filename, 'r').readlines()[line_number]

        # Find out what variable(s) we are talking about
        variable, parents = self.parse_parents(line)
        next_line = open(filename, 'r').readlines()[line_number + 1].strip()

        # If a variable has no parents, its probabilities start with table
        if next_line.startswith('table'):
            comma_sep_probs = next_line.split('table')[1].split(';')[0].strip()
            probs = [float(p) for p in comma_sep_probs.split(',')]
            df = pd.DataFrame(columns=[variable, 'prob'])

            for value, p in zip(self.values[variable], probs):
                df.loc[len(df)] = [value, p]
                self.probabilities[variable] = df
        else:
            #create dataFrame to store the variables
            df = pd.DataFrame(columns=[variable] + parents + ['prob'])

            #loop over the lines until a line is the same as "}" 
            with open(filename, 'r') as file:
                for i in range(line_number + 1):
                    file.readline()

                for line in file:
                    if '}' in line:
                        # Done reading this probability distribution
                        break
                    
                    # Get the values for the parents
                    comma_sep_values = line.split('(')[1].split(')')[0]
                    values = [v.strip() for v in comma_sep_values.split(',')]

                    # Get the probabilities for the variable
                    comma_sep_probs = line.split(')')[1].split(';')[0].strip()
                    probs = [float(p) for p in comma_sep_probs.split(',')]

                	# Create a row in the df for each value combination
                    for value, p in zip(self.values[variable], probs):
                        df.loc[len(df)] = [value] + values + [p]

            self.probabilities[variable] = df

    def parse_variable(self, line_number, filename):
        variable = open(filename, 'r').readlines()[line_number].split()[1]
        line = open(filename, 'r').readlines()[line_number+1]

        start = line.find('{') + 1
        end = line.find('}')
        
        values = [value.strip() for value in line[start:end].split(',')]
        self.values[variable] = values

    def parse_parents(self, line):
        start = line.find('(') + 1
        end = line.find(')')
        
        variables = line[start:end].strip().split('|')
        variable = variables[0].strip()

        if len(variables) > 1:
            parents = variables[1]
            self.parents[variable] = [v.strip() for v in parents.split(',')]
        else:
            self.parents[variable] = []

        return variable, self.parents[variable]

    @property
    def nodes(self):
        return list(self.values.keys())
