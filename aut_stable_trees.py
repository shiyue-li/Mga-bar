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

    return set(subset for subset in powerset(range(n)) if is_valid_subset(subset, weights))


def are_connected(subset1, subset2, n):
    # edges: S ~ T iff S < T or S < T^c or T < S or T^c < S

    subset1 = set(subset1)
    subset1_comp = set(get_complement(subset1, n))
    subset2 = set(subset2)
    subset2_comp = set(get_complement(subset2, n))

    if subset1 < subset2 or subset1 < subset2_comp:
        return True
    elif subset2 < subset1 or subset2 < subset1_comp:
        return True
    return False


def build_graph(weights):
    vertices = _get_vertices(weights)

    return Graph({subset1: [subset2 for subset2 in enumerate(vertices)
                            if are_connected(subset1, subset2, len(weights))]
                  for subset1 in enumerate(vertices)})


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
            print(f"{weights} is a counter-example")
            print(f"|Aut(G)|={aut_graph.order()}, |Aut(K)|={aut_complex.order()}")
            return

    print(f"All clear for n={n}")


if __name__ == "__main__":
    counter_example = [QQ(1 / 4), QQ(1 / 3), QQ(1 / 7), QQ(1 / 10),
                       QQ(1 / 5), QQ(1 / 2), QQ(1 / 4), QQ(1 / 4), QQ(1 / 9), QQ(1 / 6)]
    G = build_graph(counter_example)
    print(G.vertices())
