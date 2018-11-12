import functools
from to_tree import Node, output_tree
import functools
import copy

def _firstWord(tree):

    if tree.children:
        return firstWord(tree.children[0])

    else:
        return tree.name

def first_equals(tree1, tree2):
    return firstWord(tree1) == firstWord(tree2)

def _tree_equals(tree1, tree2, tolerance = 0, limit = 2):
    if tolerance > limit:
        return True
    if not tree1.children and not tree2.children:
        return True
    elif len(tree1.children) != len(tree2.children):
        return False
    else:
        return tree1.name == tree2.name and \
            all(_tree_equals(child1, child2, tolerance + 1, limit) for (child1, child2) in zip(tree1.children, tree2.children))

'''
function application:
    find where the trees are unbalanced
    look at the one with more nodes:
        combine two (may expand on this later) children through function application
    compare again, maybe starting from that subtree?
'''
def tree_equals(tree1, tree2, limit = 2):
    return _tree_equals(tree1, tree2, limit = limit)

def strict_equals(tree1, tree2):
    return tree_equals(tree1, tree2, 0, float('inf'))

'''
number of nodes below a node
'''
def _tree_weight(tree):
    if not tree.children:
        return 0
    else:
        return len(tree.children) + sum(_tree_weight(child) for child in tree.children)

def equals_with_application(tree1_, tree2):
    tree1 = copy.deepcopy(tree1_)

    w1 = _tree_weight(tree1)
    w2 = _tree_weight(tree2)

    if(w1 < w2):
        return equals_with_application(tree2, tree1)

    #find smallest subtree that's still greater
    #assumption: tree1 > tree2
    #for w1, w2, c1,c2  in map(_tree_weight, zip(tree1.children, tree2.children)):

    go_deeper = True
    while go_deeper:
        go_deeper = False
        for c1, c2 in zip(tree1.children, tree2.children):

            #go deeper
            if _tree_weight(c1) > _tree_weight(c2):
                tree1, tree2 = c1,c2
                go_deeper = True
            #for each pair of weights of children
            # else:
                # break

    #c1,c2 now point to where the trees disagree
    #c1 needs to be 'applied'
    c1 = Node("".join(child.name for child in c1.children), functools.reduce(lambda x, y: x.children + y.children, c1.children))
    output_tree(c1)

    output_tree(tree1)
    output_tree(tree2)
