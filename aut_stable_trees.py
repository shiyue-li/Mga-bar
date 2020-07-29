import sage.all
from sage.all import *

import itertools


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s) + 1))

def sum_weighted(subset, weights):
    return sum(weights[i] for i in subset)
    

def are_connected(n, subset1, subset2):
    set1 = set(subset1)
    set1_comp = set(range(n)) - set1
    set2 = set(subset2)
    set2_comp = set(range(n)) - set2

    if set1 < set2 or set2 < set1 or set1 < set2_comp or set2 < set1_comp:
        return True
    return False


def build_graph(weights):
    # vertices are subsets S where S < [n-1] where sum(S) > 1 and sum(S^c) > 1)
    # dont want to include a subset if its complement has been computed
    # (I.E. don't count (S, S^c) and (S^c, S) as the same)
    # edges: S ~ T iff S < T or S < T^c or T < S or T^c < S

    vertices = set()
    n = len(weights)

    for subset in powerset(range(n)):
        complement = tuple(sorted(set(range(n)) - set(subset)))
        if complement not in vertices:
            if sum_weighted(subset, weights) > 1 and sum_weighted(complement, weights) > 1:
                vertices.add(subset)

    edges = {idx1: [idx2 for idx2, subset2 in enumerate(vertices)
                    if are_connected(n, subset1, subset2)]
             for idx1, subset1 in enumerate(vertices)}

    return Graph(edges)


def build_complex(weights):
    return SimplicialComplex([list(subset)
                              for subset in powerset(range(len(weights)))
                              if sum_weighted(subset, weights) <= 1])


if __name__ == "__main__":
    weights = [QQ(1 / 6)] * 3 + [QQ(1 / 4)] + [QQ(1 / 2)] * 2 + [QQ(1)]

    G = build_graph(weights)
    aut_graph = G.automorphism_group()

    K = build_complex(weights)
    aut_complex = K.automorphism_group()

    print(aut_graph.is_isomorphic(aut_complex))
