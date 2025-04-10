# reef-cam-ip

To add a new camera:
1. Add the Camera Configuration
Open the config.py file and add a new entry to the CAMERAS dictionary. For example, to add a third camera:
```
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
```
# Camera 3
DEVICE_ID_CAM3=tankcam03
RTSP_URL_CAM3=rtsp://username:password@192.168.1.150:554/stream1
```
3. Restart the Application
Restart your Flask application to load the new configuration:
```
python backend/app.py
```
5. Verify in the Web Interface
Visit the web interface (e.g., http://localhost:5001/) and confirm that the new camera appears on the homepage with live video, snapshot, and timelapse functionality.
