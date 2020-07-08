from sage.graphs.trees import TreeIterator

def count_trees(trees):
    '''input: an iterator containing trees.
    output: the size of the iterator.'''
    count = 0
    for t in trees:
        count += 1
    return count


def assign_weights(T, w):
    '''
    input: a tree, and a weight vector (list).
    output: all possible weightings on T with w.
    '''

    S = Permutations(len(w))
    vert_dic = T.get_vertices()
    weighted_trees = []

    # Assign weight to leaves while permuting the weight vector entries.
    # If a vertex is a leaf, assign a weight to the vertex;
    for perm in S:
        permed_w = perm.action(w)
        index = 0
        new_vert_dic = {}
        for v in vert_dic:
            if v.degree() == 1:
                new_vert_dic[v] = permed_w[index]
                index += 1
        weighted_trees.append(new_vert_dic)
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
