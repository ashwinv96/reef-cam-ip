from flask import Flask, render_template, Response, redirect, url_for
from snapshot import take_snapshot
from camera_rtsp import generate_frames

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video_feed/<camera_id>")
def video_feed(camera_id):
    return Response(generate_frames(camera_id),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route('/snapshot/<camera_id>')
def snapshot(camera_id):
    take_snapshot(camera_id)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
