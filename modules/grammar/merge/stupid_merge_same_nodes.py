from tqdm.auto import tqdm

from modules.grammar.grammar import Grammar


def merge(grammar: Grammar):
    dct = {}
    for node in tqdm(grammar.nonterminals):
        hash = node.hash_node()
        if hash in dct:
            dct[hash] += [node]
        else:
            dct[hash] = [node]

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
    grammar.nonterminals = new_nodes


def stupid_merge_same_nodes(grammar: Grammar):
    before = len(grammar.nonterminals)
    while True:
        n = len(grammar.nonterminals)
        merge(grammar)

        if n == len(grammar.nonterminals):
            break
    return before, len(grammar.nonterminals)
