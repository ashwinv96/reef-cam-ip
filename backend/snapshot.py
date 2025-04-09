import os
import cv2
import boto3
from datetime import datetime
from dotenv import load_dotenv
from camera_rtsp import get_current_frame

load_dotenv()

S3_BUCKET = os.getenv("S3_BUCKET")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_ENDPOINT = os.getenv("S3_ENDPOINT")
USER_ID = os.getenv("USER_ID")
DEVICE_IDS = {
    "cam1": os.getenv("DEVICE_ID_CAM1", "unknown"),
    "cam2": os.getenv("DEVICE_ID_CAM2", "unknown")
}

# Initialize R2 client
s3 = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY
)

def take_snapshot(camera_id):
    frame = get_current_frame(camera_id)
    if frame is None:
        print(f"⚠️ No frame available from {camera_id}")
        return None

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H-%M-%S")
    filename = f"snapshot_{time_str}.jpg"
    local_path = f"snapshots/{camera_id}_{filename}"

    os.makedirs("snapshots", exist_ok=True)
    cv2.imwrite(local_path, frame)
    print(f"✅ Snapshot saved as {filename}")

    # Upload to R2 under user/device/camera path
    cloud_path = f"{USER_ID}/{DEVICE_IDS[camera_id]}/snapshots/{date_str}/{filename}"
    try:
        with open(local_path, "rb") as f:
            s3.upload_fileobj(f, S3_BUCKET, cloud_path)
        print(f"✅ Uploaded to R2: {cloud_path}")
    except Exception as e:
        print(f"❌ Failed to upload to R2: {e}")

    return filename
