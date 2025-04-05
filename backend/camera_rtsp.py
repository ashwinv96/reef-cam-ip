import cv2
import os

SIM_MODE = os.environ.get("USE_SIMULATION", "true").lower() == "true"
VIDEO_SOURCE = "/Users/avadivel/repos/reef-cam-ip/test_assets/reef_test.mp4"
RTSP_STREAM = "rtsp://username:password@camera-ip:554/stream1"

def get_video_capture():
    if True:
        return cv2.VideoCapture(VIDEO_SOURCE)
    return cv2.VideoCapture(RTSP_STREAM)

def generate_frames():
    cap = get_video_capture()
    if not cap.isOpened():
        print("Failed to open video source.")
        return

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Couldn't read frame.")
            break

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
