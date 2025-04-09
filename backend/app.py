from flask import Flask, render_template, Response, redirect, url_for, request, jsonify
from snapshot import take_snapshot
from camera_rtsp import generate_frames
from timelapse_utils import start_custom_timelapse_job
import threading
import time
from datetime import datetime, timedelta

app = Flask(__name__)

# Track active manual timelapse jobs and cooldowns
timelapse_locks = {}       # camera_id -> threading.Lock
timelapse_end_times = {}   # camera_id -> datetime

# Duration of the timelapse job (must match timelapse_utils)
DEFAULT_VIDEO_INTERVAL = 300  # seconds (5 mins)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video_feed/<camera_id>")
def video_feed(camera_id):
    return Response(generate_frames(camera_id),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/snapshot/<camera_id>")
def snapshot(camera_id):
    take_snapshot(camera_id)
    return redirect(url_for("index"))

@app.route("/trigger_timelapse/<camera_id>", methods=["POST"])
def trigger_timelapse(camera_id):
    snapshot_interval = int(request.form.get("snapshot_interval", 10))
    video_interval = int(request.form.get("video_interval", DEFAULT_VIDEO_INTERVAL))

    if camera_id not in timelapse_locks:
        timelapse_locks[camera_id] = threading.Lock()

    if camera_id in timelapse_end_times and datetime.now() < timelapse_end_times[camera_id]:
        print(f"⏳ Timelapse already running for {camera_id}")
        return redirect(url_for("index"))

    def run_timelapse():
        start_custom_timelapse_job(camera_id, snapshot_interval, video_interval)

    thread = threading.Thread(target=run_timelapse, daemon=True)
    thread.start()

    timelapse_end_times[camera_id] = datetime.now() + timedelta(seconds=video_interval)
    print(f"🟢 Manual timelapse started for {camera_id} (every {snapshot_interval}s, duration {video_interval}s)")
    return redirect(url_for("index"))

@app.route("/status/<camera_id>")
def timelapse_status(camera_id):
    now = datetime.now()
    end_time = timelapse_end_times.get(camera_id)

    if end_time and now < end_time:
        remaining = int((end_time - now).total_seconds())
        return jsonify({"active": True, "seconds_left": remaining})
    return jsonify({"active": False})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
