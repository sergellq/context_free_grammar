class Node:
    all_nodes = []

    def __init__(self, terminal=False, rules=None):
        self.terminal = terminal
        if rules is None:
            self.rules = []
        else:
            self.rules = rules

        if not terminal:
            self.color = len(Node.all_nodes)
            Node.all_nodes += [self]
        else:
            self.color = -rules[1] - 5

    def hash_node(self):
        hash = []
        for action, nodes in self.rules:
            hash += [(action, [x.color for x in nodes])]
        hash = sorted(hash)
        res = []
        for x, y in hash:
            res += [x]
            res += y
        return tuple(res)
