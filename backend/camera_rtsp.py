import os
import cv2
import threading
import time
from dotenv import load_dotenv
from camera_config import load_config, get_camera_rtsp

load_dotenv()

frame_buffers = {}
locks = {}
stream_threads = {}
stop_flags = {}

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

        if camera_id not in locks:
            print(f"⚠️ Camera {camera_id} has been removed. Exiting stream thread.")
            break

        with locks[camera_id]:
            frame_buffers[camera_id] = frame
    cap.release()

def start_camera(camera_id):
    if camera_id in stream_threads:
        print(f"⚠️ Camera {camera_id} already running")
        return
    rtsp_url = get_camera_rtsp(camera_id)
    if not rtsp_url:
        print(f"❌ No RTSP URL found for {camera_id}")
        return
    frame_buffers[camera_id] = None
    locks[camera_id] = threading.Lock()
    stop_flags[camera_id] = False
    thread = threading.Thread(target=stream_camera, args=(camera_id, rtsp_url), daemon=True)
    stream_threads[camera_id] = thread
    thread.start()
    print(f"🟢 Started camera stream for {camera_id}")

def stop_camera(camera_id):
    if camera_id in stop_flags:
        stop_flags[camera_id] = True
        print(f"🔁 Flag set to stop camera {camera_id}")
    stream_threads.pop(camera_id, None)
    frame_buffers.pop(camera_id, None)
    locks.pop(camera_id, None)
    stop_flags.pop(camera_id, None)

def reload_all_cameras():
    current_config = load_config()
    current_ids = set(current_config.keys())
    running_ids = set(stream_threads.keys())

    # Stop removed cameras
    for cam_id in running_ids - current_ids:
        stop_camera(cam_id)

    # Start new cameras
    for cam_id in current_ids - running_ids:
        start_camera(cam_id)

def generate_frames(camera_id):
    while True:
        with locks.get(camera_id, threading.Lock()):
            frame = frame_buffers.get(camera_id)
        if frame is None:
            time.sleep(0.1)
            continue
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

def get_current_frame(camera_id):
    with locks.get(camera_id, threading.Lock()):
        frame = frame_buffers.get(camera_id)
        return frame.copy() if frame is not None else None

# Start all at launch
reload_all_cameras()
