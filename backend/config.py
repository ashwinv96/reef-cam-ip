from dotenv import load_dotenv
import os

load_dotenv()

# Other configurations...
CAMERAS = {
    "cam1": {
        "device_id": os.getenv("DEVICE_ID_CAM1"),
        "rtsp_url": os.getenv("RTSP_URL_CAM1")
    },
    "cam2": {
        "device_id": os.getenv("DEVICE_ID_CAM2"),
        "rtsp_url": os.getenv("RTSP_URL_CAM2")
    }
}

S3_BUCKET = os.getenv("S3_BUCKET")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_ENDPOINT = os.getenv("S3_ENDPOINT")
USER_ID = os.getenv("USER_ID")

# Timelapse settings
TIMELAPSE_SNAPSHOT_INTERVAL_SEC = int(os.getenv("TIMELAPSE_SNAPSHOT_INTERVAL_SEC", 10))
TIMELAPSE_VIDEO_INTERVAL_SEC = int(os.getenv("TIMELAPSE_VIDEO_INTERVAL_SEC", 300))