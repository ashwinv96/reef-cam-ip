import os
import cv2
import threading
from dotenv import load_dotenv

load_dotenv()

CAMERA_URLS = {
    "cam1": os.getenv("RTSP_URL_CAM1"),
    "cam2": os.getenv("RTSP_URL_CAM2"),
}

frame_buffers = {
    "cam1": None,
    "cam2": None,
}
locks = {
    "cam1": threading.Lock(),
    "cam2": threading.Lock(),
}

def stream_camera(camera_id, rtsp_url):
    cap = cv2.VideoCapture(rtsp_url)
    while True:
        if not cap.isOpened():
            print(f"❌ Could not open stream for {camera_id}")
            break
        ret, frame = cap.read()
        if not ret:
            print(f"⚠️ Failed to grab frame from {camera_id}")
            break
        with locks[camera_id]:
            frame_buffers[camera_id] = frame
    cap.release()

# Start threads
for cam_id, url in CAMERA_URLS.items():
    threading.Thread(target=stream_camera, args=(cam_id, url), daemon=True).start()

def generate_frames(camera_id):
    while True:
        with locks[camera_id]:
            frame = frame_buffers[camera_id]
        if frame is None:
            continue
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

def get_current_frame(camera_id):
    with locks[camera_id]:
        frame = frame_buffers[camera_id]
        return frame.copy() if frame is not None else None
