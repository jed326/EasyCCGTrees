import sys
import copy


# basic node class
class Node:
    __slots__ = "children", "value"

    @property
    def name(self):
        return self.value

    def __init__(self, value, children=None):
        self.value = value
        if children is None:
            self.children = []
        else:
            self.children = children

    def __deepcopy__(self, memo=None):
        return Node(self.name, copy.deepcopy(self.children))

    def __str__(self):
        if len(self.children) == 0:
            return self.name
        return "{}:[{}]".format(self.name, ",".join([str(child) for child in self.children]))


# tree node for ccg parse
class CCGNode(Node):
    __slots__ = "children", "value", "node_type", "combinator"
    NON_LEAF = 'T'
    LEAF = 'L'

    @property
    def name(self):
        if self.node_type == 'T':
            return self.combinator
        else:
            return "%s %s" % (self.combinator, self.value)

    @classmethod
    def from_ccg(cls, ccg_output: str):
        node_elements = ccg_output[ccg_output.find('<') + 1:ccg_output.find('>')].split()
        node_type = node_elements[0]
        combinator = node_elements[1]
        node_children_str = ccg_output[ccg_output.find('>') + 1:ccg_output.rfind(')')]
        node_children = []
        if node_type == CCGNode.NON_LEAF:
            node_children = _bracket_split(node_children_str)
        value = node_elements[4] if node_type == CCGNode.LEAF else ''
        children = [CCGNode.from_ccg(c) for c in node_children]
        return CCGNode(value, node_type, combinator, children)

    def __init__(self, value: str, node_type: str, combinator: str, children: list = None):
        super().__init__(value, children)
        self.node_type = node_type
        self.combinator = combinator

    def __str__(self):
        if len(self.children) == 0:
            return self.name
        return "{} {}:[{}]".format(self.name, self.combinator, ",".join([str(child) for child in self.children]))

    def intersection(self, other):
        if type(other) != CCGNode:
            print(type(other))
            return None
        if self.combinator == other.combinator:
            if (self.node_type, other.node_type) == (CCGNode.NON_LEAF, CCGNode.NON_LEAF):
                return CCGNode(self.name, self.node_type, self.combinator,
                               [s.intersection(o) for s, o in zip(self.children, other.children) if
                                s.combinator == o.combinator])
            else:
                self_word_set = set(self.to_sentence().split('|'))
                other_word_set = set(other.to_sentence().split('|'))
                return CCGNode('|'.join(self_word_set.union(other_word_set)), CCGNode.LEAF, self.combinator)
        else:
            return None

    def to_sentence(self):
        if self.node_type == CCGNode.LEAF:
            return self.value
        else:
            return " ".join([c.to_sentence() for c in self.children])

    def __and__(self, other):
        return self.intersection(other)


# separates a string to a list of strings based on top-level brackets
def _bracket_split(s):
    starts = []
    ends = []
    lvl = 0
    for i, c in enumerate(s):
        if c == '(':
            if lvl == 0:
                starts.append(i)
            lvl += 1
        if c == ')':
            if lvl == 1:
                ends.append(i)
            lvl -= 1
    return [s[start:end + 1] for start, end in zip(starts, ends)]


# print tree to either screen or output to file
def output_tree(current_node, output_file=None, indent="", last='updown', limit=None):
    nb_children = lambda node: sum(nb_children(child) for child in node.children) + 1
    size_branch = {child: nb_children(child) for child in current_node.children}
    if limit is not None and limit == 0:
        return
    """ Creation of balanced lists for "up" branch and "down" branch. """
    up = sorted(current_node.children, key=lambda node: nb_children(node))
    down = []
    while up and sum(size_branch[node] for node in down) < sum(size_branch[node] for node in up):
        down.append(up.pop())

    """ Printing of "up" branch. """
    for child in up:
        next_last = 'up' if up.index(child) is 0 else ''
        next_indent = '{0}{1}{2}'.format(indent, ' ' if 'up' in last else '│', " " * len(current_node.name))
        output_tree(child, output_file=output_file, indent=next_indent, last=next_last,
                    limit=limit - 1 if limit else None)

    """ Printing of current node. """
    if last == 'up':
        start_shape = '┌'
    elif last == 'down':
        start_shape = '└'
    elif last == 'updown':
        start_shape = ' '
    else:
        start_shape = '├'

    if limit is None or limit > 1:
        if up:
            end_shape = '┤'
        elif down:
            end_shape = '┐'
        else:
            end_shape = ''
    else:
        end_shape = ''

    if output_file is None:
        print('{0}{1}{2}{3}'.format(indent, start_shape, current_node.name, end_shape))
    else:
        output_file.write('{0}{1}{2}{3}\n'.format(indent, start_shape, current_node.name, end_shape))
    """ Printing of "down" branch. """
    for child in down:
        next_last = 'down' if down.index(child) is len(down) - 1 else ''
        next_indent = '{0}{1}{2}'.format(indent, ' ' if 'down' in last else '│', " " * len(current_node.name))
        output_tree(child, output_file=output_file, indent=next_indent, last=next_last,
                    limit=limit - 1 if limit else None)


# legacy: converts a string to tree format
# recommend: use CCGNode.from_ccg directly
def to_tree(string):
    return CCGNode.from_ccg(string)


# receives a string from stdin and write tree to stdout
if __name__ == "__main__":
    data = sys.stdin.read()
    output_tree(CCGNode.from_ccg(data))
