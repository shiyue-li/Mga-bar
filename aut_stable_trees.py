import sage.all
from sage.all import *

import itertools


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r)
                                         for r in range(len(s) + 1))


def sum_weighted(subset, weights):
    return sum(weights[i] for i in subset)


def get_complement(subset, n):
    return tuple(sorted(set(range(n)) - set(subset)))


def is_valid_subset(subset, weights):
    complement = get_complement(subset, len(weights))

    sum_subset = sum_weighted(subset, weights)
    sum_complement = sum_weighted(complement, weights)

    return sum_subset > 1 and sum_complement > 1 and subset < complement


def _get_vertices(weights):
    n = len(weights)

    return [subset for subset in powerset(range(n))
            if is_valid_subset(subset, weights)]


def are_connected(subset1, subset2, n):
    # edges: S ~ T iff S < T or S < T^c or T < S or T^c < S

    S = set(subset1)
    S_comp = set(get_complement(subset1, n))
    T = set(subset2)
    T_comp = set(get_complement(subset2, n))

    return any((S < T, S < T_comp, T_comp < S, T < S))


def build_graph(weights):
    vertices = _get_vertices(weights)

    return Graph({subset1: [subset2 for subset2 in vertices
                            if are_connected(subset1, subset2, len(weights))]
                  for subset1 in vertices})


def build_complex(weights):
    return SimplicialComplex([tuple(subset)
                              for subset in powerset(range(len(weights)))
                              if sum_weighted(subset, weights) <= 1])


def generate_random_vector(n):
    vector = []
    while len(vector) < n:
        rand_rat = abs(QQ.random_element(1, 10))
        if rand_rat != 0:
            vector.append(rand_rat)
    return sorted(vector) if sum(vector) > 2 else generate_random_vector(n)


def compare_automorphism_groups(n):
    for i in range(30):
        weights = generate_random_vector(n)

        G = build_graph(weights)
        aut_graph = G.automorphism_group()

        K = build_complex(weights)
        aut_complex = K.automorphism_group()

        if G.size() > 0 and not aut_graph.is_isomorphic(aut_complex):
            return weights

    print(f"All clear for n={n}")

if __name__ == "__main__":
    weights = [1 / 10, 1 / 10, 1 / 4, 1 / 3, 1 / 2, 1]
    G = build_graph(weights)
    K = build_complex(weights)

    print(G.edges())

    aut_G = G.automorphism_group()
    aut_K = K.automorphism_group()

    are_isomorphic = aut_G.is_isomorphic(aut_K)
    print(are_isomorphic)
