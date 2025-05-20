import matplotlib.pyplot as plt
import numpy as np


def draw_imgs(data, shape: tuple = None, random: bool = False) -> None:
    """Displays a grid of image data using matplotlib.

    Args:
        data (np.ndarray): Array of image data with shape (H, W) or (N, H, W)
                           or (N, M, H, W)
        shape (tuple): Tuple of (rows, columns) for the subplot grid. Defaults to (2, 7)
        random (bool): Whether to randomly sample images from data. Defaults to False

    Returns:
        None
    """
    data = np.array(data)
    if len(data.shape) == 2:
        data = data[np.newaxis, :, :]
        shape = (1, 1)
    elif len(data.shape) == 4:
        if shape is None:
            shape = (data.shape[0], data.shape[1])
        data = data.reshape((-1, data.shape[2], data.shape[3]))
    elif len(data.shape) == 3 and shape is None:
        shape = (1, data.shape[0])

    rows, cols = shape
    num_images = rows * cols
    total = len(data)

    plt.figure(figsize=(cols * 2, rows * 2))

    if random:
        indices = np.random.choice(total, num_images, replace=False)
    else:
        indices = np.arange(num_images)

    for i, idx in enumerate(indices):
        plt.subplot(rows, cols, i + 1)
        plt.imshow(data[idx], cmap="gray" if data[idx].ndim == 2 else None)
        plt.axis("off")

    plt.tight_layout()
    plt.show()
