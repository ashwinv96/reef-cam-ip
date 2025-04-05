import cv2
import os
from datetime import datetime
from camera_rtsp import get_current_frame

SNAPSHOT_DIR = os.path.join(os.path.dirname(__file__), '..', 'snapshots')

def take_snapshot():
    frame = get_current_frame()
    if frame is None:
        return None

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"snapshot_{timestamp}.jpg"
    path = os.path.join(SNAPSHOT_DIR, filename)

    cv2.imwrite(path, frame)
    return filename
