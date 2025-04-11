import os
import unittest
from datetime import datetime
from snapshot import take_snapshot, DEVICE_IDS

class TestSnapshotPipeline(unittest.TestCase):
    def test_snapshot_and_upload(self):
        # Use first available camera from DEVICE_IDS
        camera_id = list(DEVICE_IDS.keys())[0]
        device_id = DEVICE_IDS[camera_id]

        # Take snapshot
        filename = take_snapshot(camera_id)
        self.assertIsNotNone(filename, "Snapshot failed or returned None")

        # Construct expected local path
        today = datetime.now().strftime("%Y-%m-%d")
        local_path = f"snapshots/{device_id}/{today}/{filename}"
        self.assertTrue(os.path.exists(local_path), f"Snapshot not found at {local_path}")

if __name__ == "__main__":
    unittest.main()
