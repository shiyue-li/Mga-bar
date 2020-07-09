from sage.graphs.trees import TreeIterator


### HELPERS ###

def count_trees(trees):
    '''
    input: an iterator containing trees.
    output: the size of the iterator.
    '''
    count = 0
    for t in trees:
        count += 1
    return count

def count_leaves(trees):
    '''
    input: an iterator containing trees.
    output: an iterator containing leaf counts of the trees.
    '''
    return [T.degree().count(1) for T in trees]

def assign_weights(T, w):
    '''
    input: a tree, and a weight vector (list).
    output: all possible weightings on T with w.
    '''

    # Check leaf counts match weight vector length.
    if T.degree().count(1) != len(w):
        raise Warning('Weight vector length must match leaf count.')
    else:
        S = Permutations(len(w))
        leaf_indexes = [i for i, x in enumerate(T.degree()) if x == 1]

        # Assign weight to leaves while permuting the weight vector entries.
        return [T.relabel(new_label(len(w), leaf_indexes, w, perm), inplace=False) for perm in S]


def new_label(leaf_counts, leaf_indexes, w, perm):
    '''
    input: a leaf count, an iterator containing leaf indexes, a weight vector, a permutation.
    output: an iterator of new labels using weight vector permuted by perm.
    '''
    new_w = perm.action(w)
    print(new_w)
    return [new_w[leaf_indexes.index(i)] if i in leaf_indexes else None for i in range(leaf_counts)]

def assign_weights_to_forest(trees, w):
    '''
    input: an iterator of trees on the same number of vertices, and a wegiht vector (list).
    output: all possible weightings on all trees with w.
    '''
    weighted_trees = []
    for t in trees:
        weighted_trees.append(assign_weights(t, w))
    return weighted_trees


### CREATE OF STABLE TREES OF A GIVEN WEIGHT###
# Note:
# V = E + 1
# V = I (internal vertices) + L (leaves)
# E = ((sum over I of deg v) + L) / 2 >= (3I + L ) / 2 by at least tri-valence of internal vertex
# Thus, V <= 2L - 2

# Useful test inputs
w2 = [1, 1/2]
w4= [1, 1, 1/1000, 1/1000]
pg = graphs.PetersenGraph()


def n_marked_trees(trees, n):
    '''
    input: a list of trees, an integer n
    output: trees of n leaves.
    '''
    return [x.degree().count(1) for x in trees]

def neighbor_labels(v, weighted_tree):
    '''
    input: an internal vertex, a weighted_tree
    output: a list of neighbors' labels of v;
            if a neighbor is
            (A) another internal vertex, label is 1;
            (B) a leaf, label is the label of the leaf.
    '''
    vert_dic = weighted_tree.get_vertices()
    nbhrs = weighted_tree.neighbors(v)
    return [vert_dic[u] if vert_dic[u] != None else 1 for u in nbhrs]

def is_stable(T):
    '''
    input: a weighted tree.
    output: T/F on stability.
    '''
    leaf_indexes = leaf_indexes(T)
    vert_dic = T.get_vertices()
    leaf_indexes = [i for i, x in enumerate(T.degree()) if x == 1]
    neighbors_of_everybody = [neighbor_labels(v, T) for v in T.get_vertices()]
    neighbors_of_internals = [N if (len(N) > 1) for N in neighbors_of_everybody]
    stable = [sum(N) > 2 for N in neighbors_of_internals]
    return all(stable)
