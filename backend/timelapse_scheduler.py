import os
import time
import threading
import subprocess
from datetime import datetime
from snapshot import take_snapshot

# Configurable via .env or defaults
CAMERA_IDS = os.getenv("CAMERA_IDS", "cam1,cam2").split(",")
SNAPSHOT_INTERVAL_SEC = int(os.getenv("TIMELAPSE_SNAPSHOT_INTERVAL_SEC", 10))  # e.g., 10s
VIDEO_GENERATION_INTERVAL_SEC = int(os.getenv("TIMELAPSE_GENERATION_INTERVAL_SEC", 300))  # e.g., 5min

def snapshot_worker(camera_id):
    while True:
        now = datetime.now().strftime("%H:%M:%S")
        print(f"[{now}] Taking snapshot for {camera_id}")
        take_snapshot(camera_id)
        time.sleep(SNAPSHOT_INTERVAL_SEC)

def generate_timelapse(camera_id):
    date_str = datetime.now().strftime("%Y-%m-%d")
    snapshot_dir = f"snapshots/{camera_id}/{date_str}"
    output_dir = f"timelapse/{camera_id}"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{date_str}_timelapse.mp4")

    # FFmpeg requires sorted input - we use glob pattern
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

    print(f"🎞️ Generating timelapse for {camera_id}...")
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✅ Time-lapse saved to {output_path}")

def start_snapshot_threads():
    for cam_id in CAMERA_IDS:
        thread = threading.Thread(target=snapshot_worker, args=(cam_id,), daemon=True)
        thread.start()
        print(f"🟢 Started snapshot thread for {cam_id}")

if __name__ == "__main__":
    start_snapshot_threads()
    while True:
        time.sleep(VIDEO_GENERATION_INTERVAL_SEC)
        for cam_id in CAMERA_IDS:
            generate_timelapse(cam_id)
