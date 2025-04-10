import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define camera configurations
CAMERAS = {
    "cam1": {
        "device_id": os.getenv("DEVICE_ID_CAM1", "tankcam01"),
        "rtsp_url": os.getenv("RTSP_URL_CAM1"),
    },
    "cam2": {
        "device_id": os.getenv("DEVICE_ID_CAM2", "tankcam02"),
        "rtsp_url": os.getenv("RTSP_URL_CAM2"),
    },
    # Add more cameras as needed
}

# Define other global configurations
S3_BUCKET = os.getenv("S3_BUCKET")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_ENDPOINT = os.getenv("S3_ENDPOINT")
USER_ID = os.getenv("USER_ID")