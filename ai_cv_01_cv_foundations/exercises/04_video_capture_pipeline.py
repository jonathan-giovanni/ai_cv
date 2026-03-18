# 04_video_capture_pipeline.py

# This file introduces a basic video processing pipeline with OpenCV.
#
# It covers:
# - opening a webcam or video file
# - reading frames in a loop
# - validating frame capture
# - converting frames to grayscale
# - drawing overlays
# - exiting safely
#
# This is one of the most important early steps in practical computer vision,
# because many real applications work on streams instead of single images.

from __future__ import annotations

from pathlib import Path
from typing import Union

import cv2
import numpy as np


VideoSource = Union[int, str]


def open_video_source(source: VideoSource) -> cv2.VideoCapture:
    """
    Open a webcam index or a video file path.
    """
    capture = cv2.VideoCapture(source)

    if not capture.isOpened():
        raise RuntimeError(f"Could not open video source: {source}")

    return capture


def convert_to_grayscale(frame: np.ndarray) -> np.ndarray:
    """
    Convert a frame to grayscale.
    """
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def draw_overlay(frame: np.ndarray, frame_index: int, gray_frame: np.ndarray) -> np.ndarray:
    """
    Draw simple information on the frame:
    - frame number
    - frame size
    - grayscale indicator
    """
    output = frame.copy()
    height, width = frame.shape[:2]

    cv2.putText(
        output,
        f"Frame: {frame_index}",
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2,
        cv2.LINE_AA,
    )

    cv2.putText(
        output,
        f"Size: {width}x{height}",
        (20, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2,
        cv2.LINE_AA,
    )

    cv2.putText(
        output,
        f"Gray shape: {gray_frame.shape[1]}x{gray_frame.shape[0]}",
        (20, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2,
        cv2.LINE_AA,
    )

    return output


def choose_video_source() -> VideoSource:
    """
    Choose the input source.

    Priority:
    1. a local file named sample_video.mp4 if it exists
    2. webcam index 0
    """
    current_dir = Path(__file__).resolve().parent
    sample_video = current_dir / "sample_video.mp4"

    if sample_video.exists():
        return str(sample_video)

    return 0


def process_stream(source: VideoSource) -> None:
    """
    Open the source and process frames in a loop.
    Press 'q' to exit.
    """
    capture = open_video_source(source)
    frame_index = 0

    try:
        while True:
            success, frame = capture.read()

            if not success or frame is None:
                print("No more frames available or failed to read frame.")
                break

            frame_index += 1

            gray_frame = convert_to_grayscale(frame)
            overlay_frame = draw_overlay(frame, frame_index, gray_frame)

            cv2.imshow("Original Video Frame", overlay_frame)
            cv2.imshow("Grayscale Video Frame", gray_frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                print("Exit requested by user.")
                break

    finally:
        capture.release()
        cv2.destroyAllWindows()


def main() -> None:
    source = choose_video_source()
    print(f"Opening video source: {source}")
    print("Press 'q' to exit.")

    process_stream(source)


if __name__ == "__main__":
    main()