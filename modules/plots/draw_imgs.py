import matplotlib.pyplot as plt
import numpy as np


def draw_imgs(data, shape: tuple = None) -> None:
    """Displays a grid of image data using matplotlib.

    Supports np.ndarray, list of np.ndarray, list of list of np.ndarray
        (even with variable shapes).

    Args:
        data (np.ndarray | list): Image(s) data to display.
        shape (tuple, optional): Grid shape (rows, cols). If None, inferred
                                    automatically.

    Returns:
        None
    """
    # Normalize input to flat list of images
    if isinstance(data, np.ndarray):
        if data.ndim == 2:
            data = [data]
        elif data.ndim == 3:
            data = list(data)
        elif data.ndim == 4:
            data = list(data.reshape(-1, data.shape[2], data.shape[3]))
        else:
            raise ValueError(f"Unsupported ndarray shape: {data.shape}")
    elif isinstance(data, list):
        # Flatten if list of lists
        if isinstance(data[0], list):
            data = [img for row in data for img in row]
    else:
        raise TypeError("Unsupported input type. Expected ndarray or list of ndarrays.")

    num_images = len(data)

    # Infer shape if not given
    if shape is None:
        cols = min(7, num_images)
        rows = int(np.ceil(num_images / cols))
    else:
        rows, cols = shape

    plt.figure(figsize=(cols * 2, rows * 2), facecolor="lightgray")

    for i in range(rows * cols):
        ax = plt.subplot(rows, cols, i + 1)
        if i < num_images:
            ax.imshow(data[i], cmap="gray" if data[i].ndim == 2 else None)
        ax.axis("off")
        ax.set_facecolor("lightgray")

    plt.tight_layout()
    plt.show()
