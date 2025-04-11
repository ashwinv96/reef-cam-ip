import unittest
from unittest.mock import patch, MagicMock
from snapshot import take_snapshot
from timelapse_utils import generate_timelapse
import os

class TestPipeline(unittest.TestCase):
    @patch("snapshot.get_current_frame")
    @patch("snapshot.s3.upload_fileobj")
    def test_snapshot(self, mock_upload, mock_frame):
        import numpy as np
        mock_frame.return_value = 255 * np.ones((480, 640, 3), dtype=np.uint8)
        filename = take_snapshot("cam1")
        self.assertTrue(filename.endswith(".jpg"))
        assert os.path.exists(f"snapshots/tankcam01/{filename.split('_')[1][:10]}/{filename}")

    @patch("subprocess.run")
    def test_timelapse_generation(self, mock_subprocess):
        mock_subprocess.return_value = 0
        generate_timelapse("cam1")  # Will succeed if dummy snapshots exist

if __name__ == '__main__':
    unittest.main()
