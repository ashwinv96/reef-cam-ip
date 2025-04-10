from flask import Flask, render_template, Response, redirect, url_for, request, jsonify
from config import CAMERAS, TIMELAPSE_VIDEO_INTERVAL_SEC  # Import the interval from config
from snapshot import take_snapshot
from camera_rtsp import generate_frames
from timelapse_utils import start_timelapse, stop_timelapse
from state import timelapse_states  # Import from state.py
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
        # Use TIMELAPSE_VIDEO_INTERVAL_SEC from config
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
        remaining = max(0, int((next_video_time - now).total_seconds()))  # Ensure no negative values
        return jsonify({"enabled": True, "seconds_left": remaining})
    return jsonify({"enabled": state["enabled"], "seconds_left": None})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)