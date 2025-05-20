class Node:
    def __init__(self, terminal=False, rules=None, color=None):
        self.terminal = terminal
        if rules is None:
            self.rules = []
        else:
            self.rules = rules

        if not terminal:
            self.color = color
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

    def get_usefull_memory(self):
        memory = 0
        if self.terminal:
            return 2
        else:
            for action, nodes in self.rules:
                memory += 1 + len(nodes) * 8
        return memory


def merge_nodes(a: Node, b: Node):
    if a.terminal or b.terminal:
        print("bad merge")
        return

    rules = a.rules + b.rules
    unique = {repr(item): item for item in rules}
    rules = list(unique.values())
    a.rules = rules
    b.rules = rules
