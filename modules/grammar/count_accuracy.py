import numpy as np
from tqdm.auto import tqdm

from modules.grammar.grammar import Grammar


class CountAccuracy:
    def __init__(
        self,
        grammar: Grammar,
        train: np.array,
        valid: np.array,
        wrong_train,
        wrong_valid,
    ):
        self.grammar = grammar
        self.train = train
        self.valid = valid
        self.wrong_train = wrong_train
        self.wrong_valid = wrong_valid

    def count_metrics(self, verbose: bool = False):
        res = {
            "train": self._count_accuracy(self.train, verbose),
            "valid": self._count_accuracy(self.valid, verbose),
        }
        res["wrong train"] = None
        res["wrong valid"] = None

        if isinstance(self.wrong_train, list):
            for i in range(len(self.wrong_train)):
                res[f"wrong train {i+1}"] = self._count_accuracy(self.wrong_train[i])
            res["wrong train"] = float(
                np.mean(
                    [res[f"wrong train {i+1}"] for i in range(len(self.wrong_train))]
                )
            )
        else:
            res["wrong train"] = self._count_accuracy(self.wrong_train, verbose)

        if isinstance(self.wrong_valid, list):
            for i in range(len(self.wrong_valid)):
                res[f"wrong valid {i+1}"] = self._count_accuracy(self.wrong_valid[i])
            res["wrong valid"] = float(
                np.mean(
                    [res[f"wrong valid {i+1}"] for i in range(len(self.wrong_valid))]
                )
            )
        else:
            res["wrong valid"] = self._count_accuracy(self.wrong_valid, verbose)

        return res

    def _count_accuracy(self, data, verbose: bool = False):
        accuracy = 0
        for img in tqdm(data) if verbose else data:
            if self.grammar.is_image_in_grammar(img):
                accuracy += 1
        return accuracy / len(data)
