import os
import cv2
from datetime import datetime
from camera_rtsp import get_current_frame
from camera_config import get_device_id
from config import S3_BUCKET, USER_ID
from s3_client import s3  # Shared S3 client

def take_snapshot(camera_id, upload_to_r2=True):
    frame = get_current_frame(camera_id)
    if frame is None:
        print(f"⚠️ No frame available from {camera_id}")
        return None

    device_id = get_device_id(camera_id)
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H-%M-%S")
    filename = f"snapshot_{time_str}.jpg"

    local_dir = f"snapshots/{device_id}/{date_str}"
    os.makedirs(local_dir, exist_ok=True)
    local_path = os.path.join(local_dir, filename)

    cv2.imwrite(local_path, frame)
    print(f"✅ Snapshot saved as {filename}")

    if upload_to_r2:
        cloud_path = f"{USER_ID}/{device_id}/snapshots/{date_str}/{filename}"
        with open(local_path, "rb") as f:
            s3.upload_fileobj(f, S3_BUCKET, cloud_path)
            print(f"✅ Uploaded to R2: {cloud_path}")

    return filename
