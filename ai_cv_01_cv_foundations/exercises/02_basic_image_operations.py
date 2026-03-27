# 02_basic_image_operations.py

# This file introduces common image operations used in early computer vision work:
# - resize
# - crop
# - grayscale conversion
# - blur
# - thresholding
# - edge detection
#
# The goal is to understand that most vision pipelines start with image preparation.
# Before detection, segmentation or recognition, images are often transformed
# to improve stability, readability or feature extraction quality.

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np


def build_sample_image(width: int = 640, height: int = 360) -> np.ndarray:
    """
    Create a synthetic image if no input file is found.
    """
    image = np.zeros((height, width, 3), dtype=np.uint8)
    image[:] = (20, 20, 20)

    cv2.rectangle(image, (30, 30), (220, 150), (255, 0, 0), thickness=-1)
    cv2.rectangle(image, (260, 60), (500, 210), (0, 255, 255), thickness=3)
    cv2.circle(image, (560, 80), 40, (0, 255, 0), thickness=-1)

    cv2.putText(
        image,
        "OpenCV Basics",
        (40, 320),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )
    return image


def load_or_create_image(path: Path) -> np.ndarray:
    """
    Try to load an image from disk.
    If the file is missing, generate a sample image.
    """
    if path.exists():
        image = cv2.imread(str(path))
        if image is not None:
            return image

    return build_sample_image()


def resize_image(image: np.ndarray, width: int, height: int) -> np.ndarray:
    """
    Resize the image to a fixed width and height.
    """
    return cv2.resize(image, (width, height))


def crop_center(image: np.ndarray, crop_width: int, crop_height: int) -> np.ndarray:
    """
    Crop the center region of the image.
    """
    image_height, image_width = image.shape[:2]

    start_x = max((image_width - crop_width) // 2, 0)
    start_y = max((image_height - crop_height) // 2, 0)

    end_x = start_x + crop_width
    end_y = start_y + crop_height

    return image[start_y:end_y, start_x:end_x]


def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
    """
    Convert a BGR image to grayscale.
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def blur_image(image: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    """
    Apply Gaussian blur.
    """
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)


def apply_binary_threshold(gray_image: np.ndarray, threshold: int = 120) -> np.ndarray:
    """
    Convert a grayscale image into a binary image using a threshold.
    """
    _, binary = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)
    return binary


def detect_edges(gray_image: np.ndarray, low_threshold: int = 50, high_threshold: int = 150) -> np.ndarray:
    """
    Detect image edges using Canny.
    """
    return cv2.Canny(gray_image, low_threshold, high_threshold)


def show_images_in_sequence(images: list[tuple[str, np.ndarray]]) -> None:
    """
    Display multiple images one by one.
    Press any key to move to the next one.
    """
    for title, image in images:
        cv2.imshow(title, image)
        cv2.waitKey(0)
        cv2.destroyWindow(title)


def main() -> None:
    current_dir = Path("../samples/").resolve()
    input_path = current_dir / "sample_input.jpg"

    image = load_or_create_image(input_path)

    resized = resize_image(image, width=480, height=270)
    cropped = crop_center(image, crop_width=260, crop_height=180)
    gray = convert_to_grayscale(image)
    blurred = blur_image(gray, kernel_size=7)
    binary = apply_binary_threshold(gray, threshold=100)
    edges = detect_edges(gray, low_threshold=60, high_threshold=180)

    print("Original shape:", image.shape)
    print("Resized shape:", resized.shape)
    print("Cropped shape:", cropped.shape)
    print("Gray shape:", gray.shape)
    print("Blurred shape:", blurred.shape)
    print("Binary shape:", binary.shape)
    print("Edges shape:", edges.shape)

    show_images_in_sequence(
        [
            ("Original", image),
            ("Resized", resized),
            ("Cropped", cropped),
            ("Gray", gray),
            ("Blurred", blurred),
            ("Binary Threshold", binary),
            ("Edges", edges),
        ]
    )

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()