from sage.all import *

import itertools


def powerset(num_elts):
    """powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"""
    s = list(range(num_elts))
    return itertools.chain.from_iterable(itertools.combinations(s, k)
                                         for k in range(num_elts + 1))


def sum_weighted(subset, vec_wt):
    return sum(vec_wt[k] for k in subset)


def get_complement(subset, num_elts):
    return tuple(sorted(set(range(num_elts)) - set(subset)))


def is_stable(subset, vec_wt):
    complement = get_complement(subset, len(vec_wt))

    sum_subset = sum_weighted(subset, vec_wt)
    sum_complement = sum_weighted(complement, vec_wt)

    return sum_subset > 1 and sum_complement > 1


def _get_vertices(vec_wt):
    return [subset for subset in powerset(len(vec_wt))
            if is_stable(subset, vec_wt)]


def are_connected(subset1, subset2, num_wts):
    s = set(subset1)
    t = set(subset2)
    t_comp = set(get_complement(subset2, num_wts))

    return any((s < t, s < t_comp, t_comp < s, t < s))


def build_graph(vec_wt):
    return Graph({subset1: neighbors(subset1, vec_wt)
                  for subset1 in _get_vertices(vec_wt)
                  if subset1 < get_complement(subset1, len(vec_wt))})


def neighbors(subset, vec_wt):
    return [other for other in _get_vertices(vec_wt)
            if are_connected(subset, other, len(vec_wt))
            and other < get_complement(other, len(vec_wt))]


def build_complex(vec_wts):
    return SimplicialComplex([tuple(subset)
                              for subset in powerset(len(vec_wts))
                              if sum_weighted(subset, vec_wts) <= 1])


def generate_random_vector(num_wts):
    vector = []
    while len(vector) < num_wts:
        rand_rat = abs(QQ.random_element(1, 10))
        if rand_rat != 0:
            vector.append(rand_rat)
    return sorted(vector) if sum(vector) > 2 else generate_random_vector(num_wts)


def generate_weights_two_ones(num_wts: int) -> list:
    two_ones = [1, 1]
    while len(two_ones) < num_wts:
        rand_rat = abs(QQ.random_element(10))
        if 0 < rand_rat < 1:
            two_ones.append(rand_rat)
    return sorted(two_ones)


def compare_automorphism_groups(num_wts):
    for _ in range(30):
        weights_two_ones = generate_weights_two_ones(num_wts)

        g = build_graph(weights_two_ones)
        aut_graph = g.automorphism_group()

        k = build_complex(weights_two_ones)
        aut_complex = k.automorphism_group()
        print(k.faces())

        if g.size() > 0 and not aut_graph.is_isomorphic(aut_complex):
            return weights_two_ones

    print(f"All clear for n={num_wts}")


if __name__ == "__main__":
    weights = [1 / 10, 1 / 4, 1 / 3, 1 / 2, 1, 1]
    G = build_graph(weights)
    print(G.vertices())
    K = build_complex(weights)
    print(K)

    aut_G = G.automorphism_group()
    aut_K = K.automorphism_group()

    are_isomorphic = aut_G.is_isomorphic(aut_K)
    print(are_isomorphic)
