from modules.grammar.grammar import Grammar
from modules.grammar.node import Node
from modules.plots.draw_imgs import draw_imgs


def plot_random_from_grammar(grammar: Grammar, shape=(1, 10), node: Node = None):
    if isinstance(shape, int):
        shape = (shape,)
    if len(shape) == 1:
        imgs = [grammar.sample_random(node) for _ in range(shape[0])]
        shape = (1, shape[0])
    elif len(shape) == 2:
        imgs = [
            [grammar.sample_random(node) for _ in range(shape[0])]
            for __ in range(shape[1])
        ]
    draw_imgs(imgs, shape)
