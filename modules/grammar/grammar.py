import random

import numpy as np
import pandas as pd
from tqdm.auto import tqdm

from modules.grammar.node import Node
from modules.grammar.split_metrics import dispersion_metric


class Grammar:
    def __init__(self, colors, split_metric=dispersion_metric):
        self.terminals = []
        for i in range(colors):
            self.terminals += [Node(terminal=True, rules=("1x1 pixel", i))]
        self.split_metric = split_metric
        self.root = None
        self.nonterminals = []

    def set_height_for_all_nodes(self, verbose: bool = True):
        for node in self.terminals:
            node.height = 0
        for node in self.nonterminals:
            node.height = None

        def dfs(node):
            if node.height is not None:
                return node.height
            node.height = 0
            for action, nodes in node.rules:
                for nx in nodes:
                    tmp = dfs(nx)
                    if tmp > node.height:
                        node.height = tmp
            node.height += 1
            return node.height

        dfs(self.root)

        res = [[] for _ in range(self.root.height + 1)]
        for node in self.terminals:
            res[node.height] += [node]
        for node in self.nonterminals:
            res[node.height] += [node]
        df = (
            pd.DataFrame(
                {
                    "height": np.arange(len(res)),
                    "number of nodes": [len(x) for x in res],
                }
            )
            .set_index("height")
            .T
        )
        if verbose:
            print(df)
            return res
        else:
            return res, df

    def add_images(self, images):
        if self.root is None:
            self.root = Node(color=0)
            self.nonterminals += [self.root]

        for img in tqdm(images):
            self.root.rules += [("single image", [self.build_grammar(img)])]

    def build_grammar(self, image):
        if image is None:
            raise ValueError("Input image is None.")
        if image.min() == image.max():
            return self.terminals[image.min()]

        action, images = self.split_image(image)
        children = [self.build_grammar(img) for img in images]

        node = Node(
            terminal=False, rules=[(action, children)], color=len(self.nonterminals)
        )
        self.nonterminals += [node]
        return node

    def split_image(self, image):
        n, m = image.shape

        # horizontal line
        h_value = -1
        if n > 1:
            h_value = self.split_metric(image[n // 2 - 1, :], image[n // 2, :])

        # vertical line
        v_value = -1
        if m > 1:
            v_value = self.split_metric(image[:, m // 2 - 1], image[:, m // 2])

        if h_value > v_value:
            return "horizontal line", [image[: n // 2], image[n // 2 :]]
        else:
            return "vertical line", [image[:, : m // 2], image[:, m // 2 :]]

    def sample_random(self, node=None):
        if node is None:
            node = self.root
        if node.terminal:
            if node.rules[0] == "1x1 pixel":
                return np.ones((1, 1)) * node.rules[1]
            raise ValueError("wrong terminal action")

        action, nodes = random.choice(node.rules)
        nodes = [self.sample_random(x) for x in nodes]

        n = np.max([x.shape[0] for x in nodes])
        m = np.max([x.shape[1] for x in nodes])

        for i in range(len(nodes)):
            if n % nodes[i].shape[0] != 0 or m % nodes[i].shape[1] != 0:
                raise ValueError("bad size")

            nodes[i] = np.repeat(nodes[i], n // nodes[i].shape[0], axis=0)
            nodes[i] = np.repeat(nodes[i], m // nodes[i].shape[1], axis=1)

        if action == "horizontal line":
            return np.vstack(nodes)
        elif action == "vertical line":
            return np.hstack(nodes)
        elif action == "single image":
            return nodes[0]
        else:
            raise ValueError("bad action")

    def is_image_in_grammar(self, image, node=None):
        if node is None:
            node = self.root
        if node.terminal:
            if node.rules[0] == "1x1 pixel":
                return image.min() == image.max() and image.min() == node.rules[1]
            raise ValueError(f"Unknown terminal action: {node.rules[0]}")

        for action, nodes in node.rules:
            if action == "horizontal line":
                if image.shape[0] > 1:
                    image0 = image[: image.shape[0] // 2]
                    image1 = image[image.shape[0] // 2 :]
                    if self.is_image_in_grammar(
                        image0, nodes[0]
                    ) and self.is_image_in_grammar(image1, nodes[1]):
                        return True
            elif action == "vertical line":
                if image.shape[1] > 1:
                    image0 = image[:, : image.shape[1] // 2]
                    image1 = image[:, image.shape[1] // 2 :]
                    if self.is_image_in_grammar(
                        image0, nodes[0]
                    ) and self.is_image_in_grammar(image1, nodes[1]):
                        return True
            elif action == "single image":
                if self.is_image_in_grammar(image, nodes[0]):
                    return True
            else:
                raise ValueError(f"Unknown action: {action}")
        return False

    def get_usefull_memory(self):
        memory = 0
        for node in self.terminals:
            memory += node.get_usefull_memory()
        for node in self.nonterminals:
            memory += node.get_usefull_memory()
        return memory
