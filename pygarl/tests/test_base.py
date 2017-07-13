import unittest
import os
import shutil
from pygarl.abstracts import *
from pygarl.mocks import *
from pygarl.base import *

# To execute tests, go to the project main directory and type:
# python -m unittest discover


class SampleTestCase(unittest.TestCase):
    """
    Tests to check FileGestureRecorder behaviour
    """

    def setUp(self):
        # Create a test directory if it doesn't exists
        if not os.path.exists("test_sample_dir"):
            os.makedirs("test_sample_dir")

        # Create the sample
        self.sample = Sample([[1, 2, 3], [4, 5, 6]], gesture_id="TESTSAMPLE")

    def tearDown(self):
        # Destroy the test directory
        shutil.rmtree("test_sample_dir")

        # Destroy the sample
        self.recorder = None

    def test_data_must_be_a_2_dimensional_array(self):
        self.assertRaises(ValueError, Sample, [])

    def test_save_to_file(self):
        filepath = os.path.join("test_sample_dir", "test_sample.txt")
        # Save the sample to file
        self.sample.save_to_file(filepath)

        # Open the json file
        with open(filepath) as data_file:
            data = json.load(data_file)

        self.assertEqual(data['gesture_id'], self.sample.gesture_id)
        self.assertEqual(data['data'], self.sample.data.tolist())

        # Remove the sample at the end
        os.remove(filepath)

    def test_load_from_file(self):
        # Create the sample file...

        filepath = os.path.join("test_sample_dir", "test_sample.txt")
        # Save the sample to file
        self.sample.save_to_file(filepath)

        # Load the sample
        sample = Sample.load_from_file(filepath)

        self.assertEqual(sample.gesture_id, self.sample.gesture_id)
        self.assertEqual(sample.data.tolist(), self.sample.data.tolist())

        # Remove the sample at the end
        os.remove(filepath)

    def test_scale_frames(self):
        sample = Sample(data=[[0, 0, 0], [1, 2, 4], [2, 4, 8], [3, 6, 12], [4, 8, 16]])
        self.assertEqual(sample.data.tolist(), [[0, 0, 0], [1, 2, 4], [2, 4, 8], [3, 6, 12], [4, 8, 16]])

        # Scale down the frames
        sample.scale_frames(3)

        self.assertEqual(sample.data.tolist(), [[0, 0, 0], [2, 4, 8], [4, 8, 16]])

    def test_get_linearized(self):
        sample = Sample(data=[[0, 0, 0], [1, 2, 4], [2, 4, 8]])
        self.assertEqual(sample.data.tolist(), [[0, 0, 0], [1, 2, 4], [2, 4, 8]])

        self.assertEqual(sample.get_linearized().tolist(), [[0, 0, 0, 1, 2, 4, 2, 4, 8]])
        self.assertEqual(sample.get_linearized(one_dimensional=True).tolist(), [0, 0, 0, 1, 2, 4, 2, 4, 8])


class CallbackManagerTestCase(unittest.TestCase):
    """
    Tests to check CallbackManager correct behaviour
    """
    def setUp(self):
        # Initialize the callback manager
        self.manager = CallbackManager()

    def tearDown(self):
        # Destroy the callback manager
        self.manager = None

    def test_callback_attached_correctly(self):
        receiver = MockFunctionReceiver()

        # Should not be attached initially
        self.assertFalse('my_gesture' in self.manager.callbacks)
        # Attach the function
        self.manager.attach_callback('my_gesture', receiver.receive)
        # Should be attached
        self.assertTrue('my_gesture' in self.manager.callbacks)

    def test_callback_detached_correctly(self):
        receiver = MockFunctionReceiver()

        # Attach the callback function
        self.manager.attach_callback('my_gesture', receiver.receive)
        # Should be attached
        self.assertTrue('my_gesture' in self.manager.callbacks)
        # Detach the callback function
        self.manager.detach_callback('my_gesture')
        # Should be detached
        self.assertFalse('my_gesture' in self.manager.callbacks)

    def test_callback_notify_gesture(self):
        receiver = MockFunctionReceiver()

        # Attach the callback function
        self.manager.attach_callback('my_gesture', receiver.receive)
        # Initially it's not received
        self.assertFalse(receiver.received)
        # Send the notify
        self.manager.notify_gesture('my_gesture')
        # Should be received
        self.assertTrue(receiver.received)

    def test_callback_notify_gesture_should_not_call_the_function(self):
        receiver = MockFunctionReceiver()

        self.manager.attach_callback('my_gesture', receiver.receive)
        self.assertFalse(receiver.received)
        # Notify another gesture
        self.manager.notify_gesture('not_my_gesture')
        # Should not be called
        self.assertFalse(receiver.received)

    def test_callback_receive_gesture_forward_the_event_to_the_callbacks(self):
        receiver = MockFunctionReceiver()

        self.manager.attach_callback('my_gesture', receiver.receive)
        self.assertFalse(receiver.received)
        # Simulate an event, should propagate to the attached callbacks
        self.manager.receive_gesture('my_gesture')
        self.assertTrue(receiver.received)

    def test_callback_notify_gesture_multiple_callbacks(self):
        """
        Test to verify that multiple gestures call the corresponding callbacks
        """
        receiver1 = MockFunctionReceiver()
        receiver2 = MockFunctionReceiver()

        # Attach the gestures
        self.manager.attach_callback('my_gesture', receiver1.receive)
        self.manager.attach_callback('my_gesture2', receiver2.receive)
        self.assertFalse(receiver1.received)
        self.assertFalse(receiver2.received)

        # Only the first one has been called
        self.manager.notify_gesture('my_gesture')
        self.assertTrue(receiver1.received)
        self.assertFalse(receiver2.received)

        # Both has been called
        self.manager.notify_gesture('my_gesture2')
        self.assertTrue(receiver1.received)
        self.assertTrue(receiver2.received)

if __name__ == '__main__':
    unittest.main()
