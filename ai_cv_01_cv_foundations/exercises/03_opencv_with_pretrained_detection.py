# 03_opencv_with_pretrained_detection.py

# This file introduces a first detection workflow without training a custom model.
# It uses a pre-trained Haar Cascade classifier included with OpenCV.
#
# Why this matters:
# - it teaches the structure of a detection pipeline
# - load input image
# - preprocess image
# - run detector
# - draw detections
# - inspect results
#
# This is a good transition point before moving later into YOLO-based detection.

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import cv2
import numpy as np

def load_face_detector() -> cv2.CascadeClassifier:
    """
    Load the built-in OpenCV face detector.
    """
    cascade_path = Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(str(cascade_path))

    if detector.empty():
        raise RuntimeError(f"Failed to load Haar Cascade from: {cascade_path}")
    return detector


def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
    """
    Convert image to grayscale because Haar Cascade expects grayscale input.
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def detect_faces(detector: cv2.CascadeClassifier, gray_image: np.ndarray) -> list[Sequence[int]]:
    """
    Detect faces in the grayscale image.

    Returns:
        list of rectangles in format (x, y, w, h)
    """
    detections = detector.detectMultiScale(
        gray_image,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(40, 40),
    )

    return list(detections)


def draw_detections(image: np.ndarray, detections: list[tuple[int, int, int, int]]) -> np.ndarray:
    """
    Draw bounding boxes around detected objects.
    """
    output = image.copy()

    for x, y, w, h in detections:
        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            output,
            "face",
            (x, max(y - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )

    return output


def show_result(original: np.ndarray, result: np.ndarray) -> None:
    """
    Display original and detection result.
    """
    cv2.imshow("Original", original)
    cv2.imshow("Detection Result", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main() -> None:
    current_dir = Path("../samples/").resolve()
    input_path = current_dir / "face_sample.jpg"

    # check if the file exist if not end the execution
    if not input_path.exists():
        print(f"Input file {input_path} does not exist. Please provide a valid image.")
        return

    # load the image
    image = cv2.imread(str(input_path))

    gray = convert_to_grayscale(image)

    detector = load_face_detector()
    detections = detect_faces(detector, gray)
    result = draw_detections(image, detections)

    print(f"Detections found: {len(detections)}")

    if detections:
        for index, (x, y, w, h) in enumerate(detections, start=1):
            print(f"Detection {index}: x={x}, y={y}, w={w}, h={h}")
    else:
        print("No faces detected. This may happen with synthetic or non-face images.")

    show_result(image, result)


if __name__ == "__main__":
    main()