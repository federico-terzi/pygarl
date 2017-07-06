import unittest
import os
import shutil
import scipy as sp
from pygarl.abstracts import *
from pygarl.recorders import *
from pygarl.mocks import *
from pygarl.base import *


# To execute tests, go to the project main directory and type:
# python -m unittest discover


class FileGestureRecorderTestCase(unittest.TestCase):
    """
    Tests to check FileGestureRecorder behaviour
    """

    def setUp(self):
        # Create a test directory if it doesn't exists
        if not os.path.exists("test_dir"):
            os.makedirs("test_dir")

        # Create the recorder
        self.recorder = FileGestureRecorder("test_dir")

    def tearDown(self):
        # Destroy the test directory
        shutil.rmtree("test_dir")

        # Destroy the recorder
        self.recorder = None

    def test_invalid_directory_should_raise_exception(self):
        self.assertRaises(ValueError, FileGestureRecorder, "non_existent_directory")

    def test_sample_without_gesture_id_should_raise_exception(self):
        sample = Sample([[]])

        self.assertRaises(ValueError, self.recorder.save_sample, sample)

    def test_save_sample(self):
        sample = MockSample()
        self.assertTrue(self.recorder.save_sample(sample).startswith("TESTSAMPLE_"))

        self.assertTrue("TESTSAMPLE_" in sample.file_path)

    def test_receive_sample(self):
        sample = MockSample()
        self.recorder.receive_sample(sample)

        self.assertTrue("TESTSAMPLE_" in sample.file_path)

    def test_save_sample_filenames_are_unique(self):
        sample = MockSample()
        self.recorder.save_sample(sample)
        filepath1 = sample.file_path

        self.recorder.save_sample(sample)
        filepath2 = sample.file_path

        self.assertTrue(filepath1 != filepath2)

if __name__ == '__main__':
    unittest.main()
