# backend/timelapse.py
import os
import subprocess
from datetime import datetime

def generate_timelapse(camera_id, output_dir="timelapse", snapshot_dir="snapshots"):
    date_str = datetime.now().strftime("%Y-%m-%d")
    input_pattern = f"{snapshot_dir}/{camera_id}_snapshot_*.jpg"
    output_path = f"{output_dir}/{camera_id}_{date_str}.mp4"

    os.makedirs(output_dir, exist_ok=True)

    # FFmpeg command
    command = [
        "ffmpeg",
        "-y",                      # Overwrite if exists
        "-framerate", "2",         # 2 fps for now (adjust later)
        "-pattern_type", "glob",
        "-i", input_pattern,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        output_path
    ]

    try:
        subprocess.run(command, check=True)
        print(f"🎞️  Time-lapse generated: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg error: {e}")
        return None
