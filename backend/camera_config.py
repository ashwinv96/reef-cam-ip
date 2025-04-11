import json
import os
import threading

CONFIG_FILE = os.getenv("CAMERA_CONFIG_FILE", "camera_config.json")
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
