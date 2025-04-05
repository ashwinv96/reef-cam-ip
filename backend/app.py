from flask import Flask, render_template, Response, redirect, url_for
from camera_rtsp import generate_frames
from snapshot import take_snapshot

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/snapshot')
def snapshot():
    filename = take_snapshot()
    if filename:
        print(f"✅ Snapshot saved as {filename}")
    else:
        print("❌ Snapshot failed.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
