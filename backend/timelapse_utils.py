import os
import time
import threading
import subprocess
from datetime import datetime
from snapshot import take_snapshot, DEVICE_IDS, s3, S3_BUCKET, USER_ID

def generate_timelapse(camera_id):
    device_id = DEVICE_IDS[camera_id]
    date_str = datetime.now().strftime("%Y-%m-%d")

    snapshot_dir = f"snapshots/{device_id}/{date_str}"
    output_dir = f"timelapse/{device_id}"
    os.makedirs(output_dir, exist_ok=True)

    filename = f"{date_str}_timelapse.mp4"
    output_path = os.path.join(output_dir, filename)

    input_pattern = os.path.join(snapshot_dir, "snapshot_*.jpg")
    command = [
        "ffmpeg",
        "-y",
        "-pattern_type", "glob",
        "-i", input_pattern,
        "-vf", "fps=10",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        output_path
    ]

    print(f"🎞️ Generating timelapse for {camera_id} ({device_id})...")
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if os.path.exists(output_path):
        print(f"✅ Time-lapse saved to {output_path}")
        cloud_path = f"{USER_ID}/{device_id}/timelapse/{date_str}/{filename}"
        with open(output_path, "rb") as f:
            s3.upload_fileobj(f, S3_BUCKET, cloud_path)
            print(f"✅ Uploaded time-lapse to R2: {cloud_path}")
    else:
        print(f"❌ Failed to generate timelapse for {camera_id}")

def start_custom_timelapse_job(camera_id, snapshot_interval, video_interval):
    def worker():
        start_time = time.time()
        while time.time() - start_time < video_interval:
            now = datetime.now().strftime("%H:%M:%S")
            print(f"[{now}] Taking snapshot for {camera_id}")
            take_snapshot(camera_id)
            time.sleep(snapshot_interval)

        generate_timelapse(camera_id)

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()
