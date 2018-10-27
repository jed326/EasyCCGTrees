from ete3 import Tree, TreeStyle, TextFace, add_face_to_node

def parse(expr):
    def _helper(iter):
        items = []
        for item in iter:
            if item == '(':
                result, closeparen = _helper(iter)
                if not closeparen:
                    raise ValueError("bad expression -- unbalanced parentheses")
                items.append(result)
            elif item == ')':
                return items, True
            else:
                items.append(item)
        return items, False
    return _helper(iter(expr))[0]

def combine(p):
    out = []
    tail = 0
    head = 0

    while tail < len(p):
        if isinstance(p[tail], str):
            tail += 1
        else:
            out.append("".join(p[head:tail]))
            l = combine(p[tail])
            if l != []:
                out.append(l)

            tail += 1
            head = tail
    else:
        out.append("".join(p[head:tail]))
    return out

def build(node, parse):
    for subtree in parse:
        if isinstance(subtree, list):
            new = node.add_child(name=subtree[0])
            build(new, subtree[1:])
        elif subtree.strip() != "":
            node.add_child(name=subtree)

if __name__ == "__main__":

    with open("sample.txt", "r") as file:
        f = file.readlines()

    p = parse(f[4])[0]

    c = combine(p)
    print(c)

    t = Tree()
    node = t.add_child(name=c[0])
    build(node, c[1:])

    print t

    ts = TreeStyle()
    ts.show_leaf_name = False
    def my_layout(node):
        F = TextFace(node.name, tight_text=True)
        add_face_to_node(F, node, column=0, position="branch-right")
    ts.layout_fn = my_layout

    t.show(tree_style=ts)
