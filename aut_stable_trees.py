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


def is_representative(subset, vec_wt):
    complement = get_complement(subset, len(vec_wt))

    if len(subset) < len(complement):
        return True
    return len(subset) == len(complement) and subset < complement


def is_stable(subset, vec_wt):
    complement = get_complement(subset, len(vec_wt))

    sum_subset = sum_weighted(subset, vec_wt)
    sum_complement = sum_weighted(complement, vec_wt)

    return sum_subset > 1 and sum_complement > 1


def build_graph(vec_wt):
    return Graph({subset1: neighbors(subset1, vec_wt)
                  for subset1 in _get_vertices(vec_wt)})


def neighbors(subset, vec_wt):
    return [other for other in _get_vertices(vec_wt)
            if are_connected(subset, other, len(vec_wt))]


def _get_vertices(vec_wt):
    return [subset for subset in powerset(len(vec_wt))
            if is_stable(subset, vec_wt)
            and is_representative(subset, vec_wt)]


def are_connected(subset1, subset2, num_wts):
    s = set(subset1)
    t = set(subset2)
    t_comp = set(get_complement(subset2, num_wts))

    return any((s < t, s < t_comp, t_comp < s, t < s))


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


def generate_heavy_light(num_heavy, num_light):
    denom = (num_light + 1)

    return [1 / denom] * num_light + [1] * num_heavy


def get_core(graph, vec_wts):
    core_vertices = [vertex for vertex in graph.vertices()
                     if len(vertex) == 2
                     and vec_wts[vertex[0]] < 1 and vec_wts[vertex[1]] == 1]

    core_subgraph = graph.subgraph(core_vertices)
    assert core_subgraph.is_subgraph(graph)

    return core_subgraph


def compare_automorphism_groups(num_wts):
    for _ in range(30):
        weights_two_ones = generate_weights_two_ones(num_wts)

        g = build_graph(weights_two_ones)
        aut_graph = g.automorphism_group()

        k = build_complex(weights_two_ones)
        aut_complex = k.automorphism_group()

        if g.size() > 0 and not aut_graph.is_isomorphic(aut_complex):
            return weights_two_ones

    print(f"All clear for n={num_wts}")
