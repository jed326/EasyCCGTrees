import sys


class Node:
    __slots__ = "children", "value"

    @property
    def name(self):
        return self.name

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


class CCGNode(Node):
    TREE_STRING = 123
    LINE_STRING = 124
    __slots__ = "children", "value", "node_type", "combinator", "string_type"

    @property
    def name(self):
        return "%s:%s" % (self.value, self.combinator)

    def __init__(self, ccg_output: str):
        node_elements = ccg_output[ccg_output.find('<') + 1:ccg_output.find('>')].split()
        self.node_type = node_elements[0]
        self.combinator = node_elements[1]
        node_children_str = ccg_output[ccg_output.find('>') + 1:ccg_output.rfind(')')]
        node_children = []
        if self.node_type == 'T':
            node_children = _bracket_split(node_children_str)
        super().__init__(node_elements[4] if self.node_type == 'L' else '',
                         [CCGNode(c) for c in node_children])

    def __str__(self):
        if len(self.children) == 0:
            return self.name
        return "{} {}:[{}]".format(self.name, self.combinator, ",".join([str(child) for child in self.children]))


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
        output_tree(child, output_file=output_file, indent=next_indent, last=next_last, limit=limit - 1 if limit else None)

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
        # try catch TODO 
        output_file.write('{0}{1}{2}{3}\n'.format(indent, start_shape, current_node.name, end_shape))

    """ Printing of "down" branch. """
    for child in down:
        next_last = 'down' if down.index(child) is len(down) - 1 else ''
        next_indent = '{0}{1}{2}'.format(indent, ' ' if 'down' in last else '│', " " * len(current_node.name))
        output_tree(child, output_file=output_file, indent=next_indent, last=next_last, limit=limit - 1 if limit else None)


def to_tree(string):
    return CCGNode(string)


# receives a string from stdin and write tree to stdout
if __name__ == "__main__":
    file_url = None
    ind_char = "\t"
    data = sys.stdin.read()
    output_tree(CCGNode(data))

