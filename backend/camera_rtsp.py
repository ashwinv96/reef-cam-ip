import cv2
import os
import threading

SIM_MODE = os.environ.get("USE_SIMULATION", "true").lower() == "true"
VIDEO_SOURCE = "test_assets/reef_test.mp4"
RTSP_STREAM = "rtsp://user:pass@camera-ip:554/stream1"

cap = cv2.VideoCapture(VIDEO_SOURCE if SIM_MODE else RTSP_STREAM)
lock = threading.Lock()
current_frame = None

def generate_frames():
    global current_frame
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        with lock:
            current_frame = frame.copy()

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

def get_current_frame():
    with lock:
        return current_frame.copy() if current_frame is not None else None
