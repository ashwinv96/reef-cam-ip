from config import CAMERAS
import cv2
import threading

frame_buffers = {camera_id: None for camera_id in CAMERAS}
locks = {camera_id: threading.Lock() for camera_id in CAMERAS}

def stream_camera(camera_id, rtsp_url):
    # Use GStreamer pipeline for hardware-accelerated decoding
    gst_pipeline = f"rtspsrc location={rtsp_url} ! decodebin ! videoconvert ! appsink"
    cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)
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

# Start threads for all cameras
for camera_id, config in CAMERAS.items():
    threading.Thread(target=stream_camera, args=(camera_id, config["rtsp_url"]), daemon=True).start()

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