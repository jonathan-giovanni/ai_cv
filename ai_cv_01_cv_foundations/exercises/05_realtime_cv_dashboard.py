# 05_realtime_cv_dashboard.py

# This script is a final integration exercise for the cv foundations stage.
#
# It combines the topics learned previously:
# - webcam capture
# - frame processing
# - grayscale conversion
# - Gaussian blur
# - Canny edge detection
# - drawing overlays
# - region of interest (ROI)
# - FPS calculation
# - OpenCV face detection
# - multi-view composition in a 2x2 dashboard
#
# Layout:
# - top-left:   original frame
# - top-right:  Canny edge detection
# - bottom-left: filtered / enhanced frame
# - bottom-right: face detection
#
# Controls:
# - press q to quit
# - press s to save the current dashboard frame
# - press r to toggle ROI visibility

from __future__ import annotations

from pathlib import Path
import time

import cv2
import numpy as np


WINDOW_NAME = "ai_cv - realtime cv dashboard"
OUTPUT_DIR_NAME = "captures"


def open_camera(camera_index: int = 0) -> cv2.VideoCapture:
    """
    Open the default webcam.
    """
    capture = cv2.VideoCapture(camera_index)

    if not capture.isOpened():
        raise RuntimeError(f"Could not open camera with index {camera_index}")

    return capture


def load_face_detector() -> cv2.CascadeClassifier:
    """
    Load OpenCV built-in Haar Cascade face detector.
    """
    cascade_path = Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(str(cascade_path))

    if detector.empty():
        raise RuntimeError(f"Could not load Haar Cascade: {cascade_path}")

    return detector


def resize_frame(frame: np.ndarray, width: int = 640) -> np.ndarray:
    """
    Resize a frame while preserving aspect ratio.
    """
    height, current_width = frame.shape[:2]

    if current_width == width:
        return frame

    scale = width / current_width
    new_height = int(height * scale)

    return cv2.resize(frame, (width, new_height))


def to_gray(frame: np.ndarray) -> np.ndarray:
    """
    Convert a BGR frame to grayscale.
    """
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def to_bgr(gray_frame: np.ndarray) -> np.ndarray:
    """
    Convert a grayscale frame back to BGR for dashboard composition.
    """
    return cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)


def apply_canny(frame: np.ndarray, low: int = 80, high: int = 160) -> np.ndarray:
    """
    Apply Canny edge detection to the input frame.
    """
    gray = to_gray(frame)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, low, high)
    return to_bgr(edges)


def apply_filtered_view(frame: np.ndarray) -> np.ndarray:
    """
    Apply a simple useful filter pipeline:
    - grayscale
    - gaussian blur
    - adaptive threshold

    This produces a high-contrast processed view.
    """
    gray = to_gray(frame)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    thresholded = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2,
    )

    return to_bgr(thresholded)


def detect_faces(
    detector: cv2.CascadeClassifier,
    frame: np.ndarray,
) -> list[tuple[int, int, int, int]]:
    """
    Detect faces in the frame and return rectangles as (x, y, w, h).
    """
    gray = to_gray(frame)

    faces = detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(40, 40),
    )

    return list(faces)


def draw_faces(
    frame: np.ndarray,
    faces: list[tuple[int, int, int, int]],
) -> np.ndarray:
    """
    Draw face detections on a copy of the frame.
    """
    output = frame.copy()

    for x, y, w, h in faces:
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


def draw_roi(frame: np.ndarray, enabled: bool = True) -> np.ndarray:
    """
    Draw a central region of interest.
    """
    output = frame.copy()

    if not enabled:
        return output

    height, width = output.shape[:2]

    roi_width = int(width * 0.45)
    roi_height = int(height * 0.45)

    start_x = (width - roi_width) // 2
    start_y = (height - roi_height) // 2
    end_x = start_x + roi_width
    end_y = start_y + roi_height

    cv2.rectangle(output, (start_x, start_y), (end_x, end_y), (255, 255, 0), 2)
    cv2.putText(
        output,
        "ROI",
        (start_x, max(start_y - 10, 20)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 0),
        2,
        cv2.LINE_AA,
    )

    return output


def draw_panel_label(frame: np.ndarray, label: str) -> np.ndarray:
    """
    Draw a top-left panel label.
    """
    output = frame.copy()

    cv2.rectangle(output, (10, 10), (260, 45), (0, 0, 0), thickness=-1)
    cv2.putText(
        output,
        label,
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )

    return output


def draw_global_overlay(
    dashboard: np.ndarray,
    fps: float,
    face_count: int,
    roi_enabled: bool,
) -> np.ndarray:
    """
    Draw global dashboard information.
    """
    output = dashboard.copy()

    info_lines = [
        f"FPS: {fps:.2f}",
        f"Faces: {face_count}",
        f"ROI: {'ON' if roi_enabled else 'OFF'}",
        "Keys: q=quit | s=save | r=toggle roi",
    ]

    box_x = 10
    box_y = 10
    box_width = 360
    box_height = 110

    cv2.rectangle(output, (box_x, box_y), (box_x + box_width, box_y + box_height), (0, 0, 0), thickness=-1)

    for index, line in enumerate(info_lines):
        y = box_y + 25 + index * 22
        cv2.putText(
            output,
            line,
            (box_x + 10, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

    return output


def ensure_same_size(frames: list[np.ndarray]) -> list[np.ndarray]:
    """
    Resize all frames to the same dimensions based on the first frame.
    """
    if not frames:
        return frames

    target_height, target_width = frames[0].shape[:2]
    result: list[np.ndarray] = []

    for frame in frames:
        resized = cv2.resize(frame, (target_width, target_height))
        result.append(resized)

    return result


def compose_dashboard(
    top_left: np.ndarray,
    top_right: np.ndarray,
    bottom_left: np.ndarray,
    bottom_right: np.ndarray,
) -> np.ndarray:
    """
    Compose a 2x2 dashboard from four equally sized frames.
    """
    frames = ensure_same_size([top_left, top_right, bottom_left, bottom_right])

    top_row = np.hstack((frames[0], frames[1]))
    bottom_row = np.hstack((frames[2], frames[3]))

    return np.vstack((top_row, bottom_row))


def save_dashboard_image(dashboard: np.ndarray, output_dir: Path) -> Path:
    """
    Save the current dashboard frame to disk.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"dashboard_{timestamp}.jpg"
    cv2.imwrite(str(output_path), dashboard)
    return output_path


def main() -> None:
    capture = open_camera(0)
    detector = load_face_detector()

    current_dir = Path("../").resolve()
    output_dir = current_dir / OUTPUT_DIR_NAME

    roi_enabled = True
    previous_time = time.perf_counter()

    try:
        while True:
            success, frame = capture.read()

            if not success or frame is None:
                print("Failed to read frame from camera.")
                break

            frame = resize_frame(frame, width=640)

            original_view = draw_roi(frame, enabled=roi_enabled)
            original_view = draw_panel_label(original_view, "Original")

            canny_view = apply_canny(frame)
            canny_view = draw_roi(canny_view, enabled=roi_enabled)
            canny_view = draw_panel_label(canny_view, "Canny")

            filtered_view = apply_filtered_view(frame)
            filtered_view = draw_roi(filtered_view, enabled=roi_enabled)
            filtered_view = draw_panel_label(filtered_view, "Filtered")

            faces = detect_faces(detector, frame)
            face_view = draw_faces(frame, faces)
            face_view = draw_roi(face_view, enabled=roi_enabled)
            face_view = draw_panel_label(face_view, "Face Detection")

            dashboard = compose_dashboard(
                original_view,
                canny_view,
                filtered_view,
                face_view,
            )

            current_time = time.perf_counter()
            elapsed = current_time - previous_time
            previous_time = current_time

            fps = 1.0 / elapsed if elapsed > 0 else 0.0

            dashboard = draw_global_overlay(
                dashboard,
                fps=fps,
                face_count=len(faces),
                roi_enabled=roi_enabled,
            )

            cv2.imshow(WINDOW_NAME, dashboard)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                print("Exit requested by user.")
                break

            if key == ord("r"):
                roi_enabled = not roi_enabled

            if key == ord("s"):
                saved_path = save_dashboard_image(dashboard, output_dir)
                print(f"Dashboard saved to: {saved_path}")

    finally:
        capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()