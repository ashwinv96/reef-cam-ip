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
    "cam1": os.getenv("DEVICE_ID_CAM1", "tankcam01"),
    "cam2": os.getenv("DEVICE_ID_CAM2", "tankcam02")
}

s3 = boto3.client("s3",
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY
)

def take_snapshot(camera_id):
    frame = get_current_frame(camera_id)
    if frame is None:
        print(f"⚠️ No frame available from {camera_id}")
        return None

    device_id = DEVICE_IDS[camera_id]
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H-%M-%S")
    filename = f"snapshot_{time_str}.jpg"

    local_dir = f"snapshots/{device_id}/{date_str}"
    os.makedirs(local_dir, exist_ok=True)
    local_path = os.path.join(local_dir, filename)

    cloud_path = f"{USER_ID}/{device_id}/snapshots/{date_str}/{filename}"

    cv2.imwrite(local_path, frame)
    print(f"✅ Snapshot saved as {filename}")

    with open(local_path, "rb") as f:
        s3.upload_fileobj(f, S3_BUCKET, cloud_path)
        print(f"✅ Uploaded to R2: {cloud_path}")

    return filename
