# tests/test_pipeline.py

import unittest
from snapshot import take_snapshot
from camera_config import get_camera_ids

class TestSnapshotPipeline(unittest.TestCase):
    def test_snapshot_for_each_camera(self):
        camera_ids = get_camera_ids()
        self.assertGreater(len(camera_ids), 0, "No cameras configured!")

        for cam_id in camera_ids:
            print(f"📸 Testing snapshot for {cam_id}")
            result = take_snapshot(cam_id, upload_to_r2=False)
            self.assertIsNotNone(result, f"Snapshot failed for {cam_id}")

if __name__ == "__main__":
    unittest.main()
