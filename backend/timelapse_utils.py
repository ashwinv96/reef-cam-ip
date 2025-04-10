import os
import time
import threading
import subprocess
from datetime import datetime, timedelta
from config import CAMERAS, S3_BUCKET, USER_ID, TIMELAPSE_VIDEO_INTERVAL_SEC
from snapshot import take_snapshot
from state import timelapse_states  # Import from state.py
from s3_client import s3  # Import the shared S3 client

timelapse_threads = {}

def start_timelapse(camera_id):
    def timelapse_worker():
        while timelapse_states[camera_id]["enabled"]:
            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            snapshot_dir = f"snapshots/{CAMERAS[camera_id]['device_id']}/{date_str}"
            os.makedirs(snapshot_dir, exist_ok=True)

            # Generate snapshots
            for _ in range(30):  # Example: 30 snapshots per video interval
                if not timelapse_states[camera_id]["enabled"]:
                    return  # Exit if timelapse is disabled
                take_snapshot(camera_id, upload_to_r2=False)
                time.sleep(10)  # Snapshot interval

            # Generate video
            generate_timelapse(camera_id)

            # Update next_video_time after generating the video
            timelapse_states[camera_id]["next_video_time"] = datetime.now() + timedelta(seconds=TIMELAPSE_VIDEO_INTERVAL_SEC)

    # Start the timelapse thread if not already running
    if camera_id not in timelapse_threads or not timelapse_threads[camera_id].is_alive():
        timelapse_states[camera_id]["enabled"] = True
        timelapse_states[camera_id]["next_video_time"] = datetime.now() + timedelta(seconds=TIMELAPSE_VIDEO_INTERVAL_SEC)  # Initial video time
        thread = threading.Thread(target=timelapse_worker, daemon=True)
        timelapse_threads[camera_id] = thread
        thread.start()

def stop_timelapse(camera_id):
    if camera_id in timelapse_threads:
        # Stop the thread by disabling the state and removing it from the dictionary
        timelapse_states[camera_id]["enabled"] = False
        del timelapse_threads[camera_id]

def generate_timelapse(camera_id):
    device_id = CAMERAS[camera_id]["device_id"]
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

    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if os.path.exists(output_path):
        cloud_path = f"{USER_ID}/{device_id}/timelapse/{date_str}/{filename}"
        with open(output_path, "rb") as f:
            s3.upload_fileobj(f, S3_BUCKET, cloud_path)
            print(f"✅ Uploaded timelapse video to R2: {cloud_path}")