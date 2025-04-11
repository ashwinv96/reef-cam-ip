from flask import Flask, render_template, Response, redirect, url_for, request, jsonify
from config import CAMERAS, TIMELAPSE_VIDEO_INTERVAL_SEC
from snapshot import take_snapshot
from camera_rtsp import generate_frames, reload_all_cameras
from timelapse_utils import start_timelapse, stop_timelapse
from state import timelapse_states
from camera_config import load_config, save_config, get_camera_ids
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", cameras=CAMERAS)

@app.route("/video_feed/<camera_id>")
def video_feed(camera_id):
    return Response(generate_frames(camera_id),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/snapshot/<camera_id>")
def snapshot(camera_id):
    take_snapshot(camera_id)
    return redirect(url_for("index"))

@app.route("/toggle_timelapse/<camera_id>", methods=["POST"])
def toggle_timelapse(camera_id):
    data = request.get_json()
    enable = data.get("enable", False)

    if enable:
        start_timelapse(camera_id)
        timelapse_states[camera_id]["enabled"] = True
        timelapse_states[camera_id]["next_video_time"] = datetime.now() + timedelta(seconds=TIMELAPSE_VIDEO_INTERVAL_SEC)
    else:
        stop_timelapse(camera_id)
        timelapse_states[camera_id]["enabled"] = False
        timelapse_states[camera_id]["next_video_time"] = None

    return jsonify({"success": True})

@app.route("/status/<camera_id>")
def timelapse_status(camera_id):
    state = timelapse_states[camera_id]
    now = datetime.now()
    next_video_time = state.get("next_video_time")

    if state["enabled"] and next_video_time:
        remaining = max(0, int((next_video_time - now).total_seconds()))
        return jsonify({"enabled": True, "seconds_left": remaining})
    return jsonify({"enabled": state["enabled"], "seconds_left": None})

# ✅ Manage Cameras UI
@app.route("/manage_cameras", methods=["GET", "POST"])
def manage_cameras():
    if request.method == "POST":
        config = load_config()
        camera_id = request.form.get("camera_id")
        rtsp_url = request.form.get("rtsp_url")
        device_id = request.form.get("device_id")

        if camera_id and rtsp_url and device_id:
            config[camera_id] = {"rtsp_url": rtsp_url, "device_id": device_id}
            save_config(config)
            reload_all_cameras()  # 🔄 Apply changes live

        return redirect(url_for("manage_cameras"))

    config = load_config()
    return render_template("manage_cameras.html", cameras=config)

# ✅ Remove Camera
@app.route("/remove_camera/<camera_id>", methods=["POST"])
def remove_camera(camera_id):
    config = load_config()
    if camera_id in config:
        del config[camera_id]
        save_config(config)
        reload_all_cameras()  # 🔄 Apply changes live
    return redirect(url_for("manage_cameras"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
