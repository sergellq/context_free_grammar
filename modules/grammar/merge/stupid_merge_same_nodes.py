from tqdm.auto import tqdm

from modules.grammar.node import Node


def merge():
    dct = {}
    for i in tqdm(range(len(Node.all_nodes))):
        hash = Node.all_nodes[i].hash_node()
        if hash in dct:
            dct[hash] += [Node.all_nodes[i]]
        else:
            dct[hash] = [Node.all_nodes[i]]

    new_color = {}
    new_nodes = []
    # recolor dict
    for hash in dct:
        new_nodes += [dct[hash][0]]
        for x in dct[hash]:
            new_color[x.color] = new_nodes[-1]
    # new rules
    for k in range(len(new_nodes)):
        for j in range(len(new_nodes[k].rules)):
            for i in range(len(new_nodes[k].rules[j][1])):
                if new_nodes[k].rules[j][1][i].color >= 0:
                    new_nodes[k].rules[j][1][i] = new_color[
                        new_nodes[k].rules[j][1][i].color
                    ]
    # new colors
    for i in range(len(new_nodes)):
        new_nodes[i].color = i
    Node.all_nodes = new_nodes


def stupid_merge_same_nodes(grammar):
    before = len(Node.all_nodes)
    while True:
        n = len(Node.all_nodes)
        merge()

        if n == len(Node.all_nodes):
            break
    return before, len(Node.all_nodes)
