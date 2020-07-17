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
    counts = []
    for T in trees:
        print(T)
        counts.append(T.degree().count(1))
    L =  [T for T in trees]
    return counts

def new_label(vert_count, leaf_indexes, w, perm):
    '''
    input: the number of vertices, an iterator containing leaf indexes, a weight vector, a permutation.
    output: an iterator of new labels using weight vector permuted by perm.
    '''
    new_w = perm.action(w)
    new_l = []
    for i in range(vert_count):
        if i in leaf_indexes:
            new_l.append(new_w[leaf_indexes.index(i)])
        else:
            new_l.append(None)
    return new_l

def assign_weights(T, w):
    '''
    input: a tree, and a weight vector (list).
    output: all possible weightings on T with w.
    '''

    # Check leaf counts match weight vector length.
    if T.degree().count(1) != len(w):
        raise Warning('Weight vector length must match leaf count.')
    else:
        weighted_trees = []
        S = Permutations(len(w))
        leaf_indexes = [i for i, x in enumerate(T.degree()) if x == 1]
        for perm in S:
            label = new_label(len(T.get_vertices()),leaf_indexes, w, perm)
            new_T = T
            for i in range(len(label)):
                print('index', i, 'label', label[i])
                new_T.set_vertex(i, label[i])
            weighted_trees.append(new_T)
        # Assign weight to leaves while permuting the weight vector entries.
        return weighted_trees

def assign_weights_to_forest(trees, w):
    '''
    input: an iterator of trees on the same number of vertices, and a wegiht vector (list).
    output: all possible weightings on all trees with w.
    '''
    weighted_trees = []
    for t in trees:
        weighted_trees.append(assign_weights(t, w))
    return weighted_trees

def draw_forest(forest):
    '''
    input: a forest.
    output: plots of the forest.
    '''
    for T in forest:
        g = T.plot()
        g.show()

def chop_trees(trees, n):
    '''
    input: a list of trees, an integer n
    output: trees of n leaves.

    (chop trees that do not have exactly n leaves)
    '''
    n_leaf_forest = []
    for T in trees:
        if T.degree().count(1) == n:
            n_leaf_forest.append(T)
    return n_leaf_forest

def n_leaf_forest(L):
    '''
    input: an integer L.
    output: an Iterator of trees with precisely n leaves.
    '''
    forest = []
    for V in range(1, 2*L-1):
        trees = TreeIterator(V)
        for T in trees:
            forest.append(T)
    n_leaf_forest = chop_trees(forest, L)
    return n_leaf_forest

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

def chop_same_trees(F):
    '''
    input: a forest F.
    output: a forest F' with duplicates removed.
    '''
    immutables = [x.copy(immutable=True) for x in F]
    new_F = list(dict.fromkeys(immutables))
    return new_F

### CREATE OF STABLE TREES OF A GIVEN WEIGHT###
# Note:
# V = E + 1
# V = I (internal vertices) + L (leaves)
# E = ((sum over I of deg v) + L) / 2 >= (3I + L ) / 2 by at least tri-valence of internal vertex
# Thus, V <= 2L - 2

# Useful test inputs
LM4 = [1, 1, 1/1000, 1/1000] # losev manin wv of size 4
LM5 = [1, 1, 1/1000, 1/1000, 1/1000] # losev manin wv of size 5

pg = graphs.PetersenGraph()
F2 = TreeIterator(2)
F3 = TreeIterator(3)
F4 = TreeIterator(4)
FL5 = n_leaf_forest(5)

def is_stable(T):
        '''
        input: a weighted tree.
        output: T/F on stability.
        '''
        leaf_indexes = leaf_indexes(T)
        vert_dic = T.get_vertices()
        leaf_indexes = [i for i, x in enumerate(T.degree()) if x == 1]
        neighbors_of_everybody = [neighbor_labels(v, T) for v in T.get_vertices()]
        print(neighbors_of_everybody)
        # neighbors_of_internals = [N if (len(N) > 1) for N in neighbors_of_everybody]
        # stable = [sum(N) > 2 for N in neighbors_of_internals]
        # return all(stable)
