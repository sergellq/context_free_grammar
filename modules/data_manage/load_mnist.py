import urllib.request

import numpy as np


def load_mnist(size: int = 1e9):
    """Loads the MNIST dataset.

    Returns:
        Tuple of Numpy arrays: (x_train, y_train, x_test, y_test).
    """
    # URL с датасетом
    url = "https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz"
    local_filename = "data/mnist.npz"

    # Скачивание файла (если он ещё не скачан)
    urllib.request.urlretrieve(url, local_filename)

    # Загрузка данных из .npz файла
    with np.load(local_filename) as data:
        x_train = data["x_train"]
        y_train = data["y_train"]
        x_test = data["x_test"]
        y_test = data["y_test"]

    x_train = (x_train >= 128).astype(int)
    x_test = (x_test >= 128).astype(int)

    x_train = np.pad(x_train, ((0, 0), (0, 4), (0, 4)))
    x_test = np.pad(x_test, ((0, 0), (0, 4), (0, 4)))

    x_train = x_train[:size]
    y_train = y_train[:size]
    x_test = x_test[:size]
    y_test = y_test[:size]

    # Проверка форм
    print("Train:", x_train.shape, y_train.shape)
    print("Test: ", x_test.shape, y_test.shape)

    return x_train, y_train, x_test, y_test
