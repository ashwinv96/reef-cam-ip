from config import CAMERAS

# Initialize timelapse states with default values
timelapse_states = {
    camera_id: {"enabled": False, "next_video_time": None} for camera_id in CAMERAS
}