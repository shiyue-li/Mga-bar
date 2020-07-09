from sage.graphs.trees import TreeIterator

def count_trees(trees):
    '''input: an iterator containing trees.
    output: the size of the iterator.'''
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
