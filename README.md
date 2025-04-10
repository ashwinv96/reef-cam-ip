# reef-cam-ip

To add a new camera:
1. Add the Camera Configuration  
Open the config.py file and add a new entry to the CAMERAS dictionary. For example, to add a third camera:
```python
CAMERAS = {
    "cam1": {
        "device_id": os.getenv("DEVICE_ID_CAM1", "tankcam01"),
        "rtsp_url": os.getenv("RTSP_URL_CAM1"),
    },
    "cam2": {
        "device_id": os.getenv("DEVICE_ID_CAM2", "tankcam02"),
        "rtsp_url": os.getenv("RTSP_URL_CAM2"),
    },
    "cam3": {  # Add the new camera here
        "device_id": os.getenv("DEVICE_ID_CAM3", "tankcam03"),
        "rtsp_url": os.getenv("RTSP_URL_CAM3"),
    },
}
```

2. Update the .env File  
Add the environment variables for the new camera in the .env file:
```env
# Camera 3
DEVICE_ID_CAM3=tankcam03
RTSP_URL_CAM3=rtsp://username:password@192.168.1.150:554/stream1
```

3. Restart the Application  
Restart your Flask application to load the new configuration:
```bash
python backend/app.py
```

4. Verify in the Web Interface  
Visit the web interface (e.g., http://localhost:5001/) and confirm that the new camera appears on the homepage with live video, snapshot, and timelapse functionality.

---

## Running the Code on the Jetson Nano

You can deploy your existing code to the Jetson Nano, but you need to ensure the following:

### a. Install Required Dependencies
The Jetson Nano runs a Linux-based OS (JetPack), so you'll need to install the necessary dependencies:

1. **Python 3 and required libraries:**
   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-pip
   pip3 install flask opencv-python boto3
   ```

2. **FFmpeg for timelapse generation:**
   ```bash
   sudo apt-get install ffmpeg
   ```

3. **GStreamer (optional, for hardware-accelerated decoding):**
   ```bash
   sudo apt-get install gstreamer1.0-tools gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly
   ```

---

### b. Enable Hardware-Accelerated Decoding
The Jetson Nano supports hardware-accelerated H.264 decoding via its GPU. Modify your code to use **GStreamer** with OpenCV for decoding RTSP streams.

**Update `camera_rtsp.py`:**
```python
import cv2

def stream_camera(camera_id, rtsp_url):
    # Use GStreamer pipeline for hardware-accelerated decoding
    gst_pipeline = f"rtspsrc location={rtsp_url} ! decodebin ! videoconvert ! appsink"
    cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)
    if not cap.isOpened():
        print(f"❌ Could not open stream for {camera_id}")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"⚠️ Failed to grab frame from {camera_id}")
            break
        # Process the frame (e.g., store in buffer, display, etc.)
        # ...
    cap.release()
```

This ensures that the Jetson Nano's GPU handles the decoding, reducing CPU load and improving performance.

---

### 3. Testing on the Jetson Nano

To validate the performance:

1. **Run the Application:**
   ```bash
   python3 backend/app.py
   ```

2. **View the Streams:**
   - Open the web interface on your MacBook Pro, phone, or Windows laptop.
   - Navigate to `http://<jetson_ip>:5001/` (replace `<jetson_ip>` with the Jetson Nano's IP address).
   - Monitor the framerate and latency of the video streams.

3. **Monitor Resource Usage:**
   - Use `htop` or `tegrastats` on the Jetson Nano to monitor CPU, GPU, and memory usage:
     ```bash
     sudo apt-get install htop
     htop
     ```
     ```bash
     sudo tegrastats
     ```

4. **Adjust Settings if Needed:**
   - Reduce the resolution or bitrate of the RTSP streams in the camera settings if the Jetson Nano struggles to maintain real-time performance.
   - Test with fewer cameras initially (e.g., 2 cameras) and scale up to 4 to find the optimal configuration.