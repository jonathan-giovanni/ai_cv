# 01_image_io_and_display.py

# This file introduces the first essential OpenCV concepts:
# - reading an image from disk
# - validating if the image exists
# - inspecting image shape
# - understanding width, height and channels
# - displaying an image in a window
# - saving an image copy
#
# This is the most basic and important starting point in computer vision:
# before applying transformations or models, you must know how to load,
# inspect and visualize image data correctly.

from __future__ import annotations

from pathlib import Path
from typing import Optional

import cv2
import numpy as np


def build_sample_image(width: int = 640, height: int = 360) -> np.ndarray:
    """
    Create a simple synthetic image so the script can run even when no file is available.

    The image contains:
    - a dark background
    - a rectangle
    - a circle
    - text
    """
    image = np.zeros((height, width, 3), dtype=np.uint8)

    image[:] = (30, 30, 30)
    cv2.rectangle(image, (40, 40), (220, 180), (0, 200, 255), thickness=2)
    cv2.circle(image, (320, 180), 60, (0, 255, 0), thickness=-1)
    cv2.putText(
        image,
        "ai_cv foundations",
        (40, 320),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )
    return image


def load_image(path: Path) -> Optional[np.ndarray]:
    """
    Load an image from disk.

    Returns:
        numpy.ndarray if the image is loaded successfully
        None if the file cannot be read
    """
    if not path.exists():
        return None

    image = cv2.imread(str(path))
    return image


def describe_image(image: np.ndarray) -> dict[str, int]:
    """
    Inspect the image shape and return width, height and channels.

    OpenCV images are NumPy arrays and usually follow:
    (height, width, channels)
    """
    if image.ndim == 2:
        height, width = image.shape
        channels = 1
    else:
        height, width, channels = image.shape

    return {
        "width": width,
        "height": height,
        "channels": channels,
    }


def save_image_copy(output_path: Path, image: np.ndarray) -> bool:
    """
    Save an image copy to disk.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return cv2.imwrite(str(output_path), image)


def show_image(window_name: str, image: np.ndarray) -> None:
    """
    Display an image until the user presses any key.
    """
    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main() -> None:
    current_dir = Path("../samples/").resolve()
    input_path = current_dir / "sample_input.jpg"
    output_path = current_dir / "sample_output_copy.jpg"

    image = load_image(input_path)

    if image is None:
        print(f"Image not found at: {input_path}")
        print("Creating a synthetic sample image instead.")
        image = build_sample_image()

    info = describe_image(image)

    print("Image loaded successfully")
    print(f"Width: {info['width']}")
    print(f"Height: {info['height']}")
    print(f"Channels: {info['channels']}")
    print(f"Data type: {image.dtype}")

    saved = save_image_copy(output_path, image)
    print(f"Image copy saved: {saved}")
    print(f"Output path: {output_path}")

    show_image("01 - Image IO and Display", image)


if __name__ == "__main__":
    main()