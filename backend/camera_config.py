import json
import os
import threading

# Use environment variable override if present (e.g., during CI)
CONFIG_FILE = os.environ.get("CAMERA_CONFIG_FILE")

# Fallback to default if not provided
if not CONFIG_FILE:
    filename = "camera_config.test.json" if os.getenv("TESTING") == "1" else "camera_config.json"
    CONFIG_FILE = os.path.join(os.path.dirname(__file__), filename)

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
