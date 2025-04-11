import json
import os
import threading

# Detect test mode and adjust filename accordingly
FILENAME = "camera_config.test.json" if os.getenv("TESTING") == "1" else "camera_config.json"

# Always resolve relative to the current file location
CONFIG_FILE = os.path.join(os.path.dirname(__file__), FILENAME)

_lock = threading.Lock()

def load_config():
    with _lock:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)

def save_config(config):
    with _lock:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)

def get_camera_ids():
    return list(load_config().keys())

def get_camera_rtsp(camera_id):
    return load_config().get(camera_id, {}).get("rtsp_url")

def get_device_id(camera_id):
    return load_config().get(camera_id, {}).get("device_id")
