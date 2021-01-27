import itertools

def get_permutations(size):
    permutations = set()
    for comb in itertools.combinations_with_replacement([True, False], size):
        for perm in itertools.permutations(comb):
            permutations.add(perm)
    return list(permutations)
