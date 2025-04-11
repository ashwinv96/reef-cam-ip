# tests/test_pipeline.py

import unittest
import numpy as np
from unittest.mock import patch
from snapshot import take_snapshot
from camera_config import get_camera_ids

class TestSnapshotPipeline(unittest.TestCase):
    @patch("camera_rtsp.get_current_frame")
    def test_snapshot_for_each_camera(self, mock_get_frame):
        # Create a dummy frame (black image)
        dummy_frame = (255 * np.ones((480, 640, 3), dtype=np.uint8))
        mock_get_frame.return_value = dummy_frame

        camera_ids = get_camera_ids()
        self.assertGreater(len(camera_ids), 0, "No cameras configured!")

        for cam_id in camera_ids:
            print(f"📸 Testing snapshot for {cam_id}")
            result = take_snapshot(cam_id, upload_to_r2=False)  # skip R2 upload
            self.assertIsNotNone(result, f"Snapshot failed for {cam_id}")

if __name__ == "__main__":
    unittest.main()
