#!/usr/local/anaconda3/bin/python3
import sys

class Node:
    __slots__ = "children", "name"
    def __init__(self,name,children=None):
        self.name = name
        if children is None:
            self.children = []
        else:
            self.children = children

def print_tree(current_node, indent="", last='updown'):
    nb_children = lambda node: sum(nb_children(child) for child in node.children) + 1
    size_branch = {child: nb_children(child) for child in current_node.children}

    """ Creation of balanced lists for "up" branch and "down" branch. """
    up = sorted(current_node.children, key=lambda node: nb_children(node))
    down = []
    while up and sum(size_branch[node] for node in down) < sum(size_branch[node] for node in up):
        down.append(up.pop())

    """ Printing of "up" branch. """
    for child in up:
        next_last = 'up' if up.index(child) is 0 else ''
        next_indent = '{0}{1}{2}'.format(indent, ' ' if 'up' in last else '│', " " * len(current_node.name))
        print_tree(child, indent=next_indent, last=next_last)

    """ Printing of current node. """
    if last == 'up': start_shape = '┌'
    elif last == 'down': start_shape = '└'
    elif last == 'updown': start_shape = ' '
    else: start_shape = '├'

    if up: end_shape = '┤'
    elif down: end_shape = '┐'
    else: end_shape = ''

    print('{0}{1}{2}{3}'.format(indent, start_shape, current_node.name, end_shape))

    """ Printing of "down" branch. """
    for child in down:
        next_last = 'down' if down.index(child) is len(down) - 1 else ''
        next_indent = '{0}{1}{2}'.format(indent, ' ' if 'down' in last else '│', " " * len(current_node.name))
        print_tree(child, indent=next_indent, last=next_last)

def to_tree(string):
    fb = string.find("(")
    lb = string.rfind(")")
    if fb == -1 or lb == -1:
        print(string,"is end")
        return Node(string)
    else:
        string_in = string[fb+1:lb]
        fpos = string_in.find("(")
        if fpos != -1:
            node = Node(string_in[:fpos])
        else:
            return Node(string_in)
        lvl = 0
        lpos = []
        rpos = []
        for i,c in enumerate(string_in):
            if c == '(':
                if lvl == 0:
                    lpos.append(i)
                lvl += 1
            elif c == ')':
                lvl -= 1
                if lvl == 0:
                    rpos.append(i)
        node.children = [to_tree(string_in[l:r+1]) for l,r in zip(lpos,rpos)]
        return node

def conv_bracket(s, lbracket_rep, rbracket_rep):
    inside = False
    new = ""
    for i,c in enumerate(s):
        if c == '<':
            inside = True
        elif c == '>':
            inside = False
        if c == '(' and inside:
            new+=lbracket_rep
        elif c == ')' and inside:
            new+=rbracket_rep
        else:
            new+=c
    return new

# example:
# java -jar easyccg.jar --model model_qstions -s -r S[q] S[qem] S[wq] | python prettify_stdin.py
if __name__ == "__main__":
    file_url = None
    ind_char = "\t"
    data = sys.stdin.read()
    data = conv_bracket(data, '<', '>')
    print_tree(to_tree(data))
