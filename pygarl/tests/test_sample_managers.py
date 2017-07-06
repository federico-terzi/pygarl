import unittest
import scipy as sp

from pygarl.sample_managers import DiscreteSampleManager, StreamSampleManager
from pygarl.abstracts import *
from pygarl.mocks import *
from pygarl.base import *

# To execute tests, go to the project main directory and type:
# python -m unittest discover


class DiscreteSampleManagerTestCase(unittest.TestCase):
    """
    Tests to check DiscreteSampleManager behaviour
    """
    def setUp(self):
        # Initialize the DiscreteSampleManager
        self.manager = DiscreteSampleManager()

    def tearDown(self):
        # Destroy the sample manager
        self.manager = None

    def test_sample_received_correctly(self):
        # Initialize a Mock Receiver
        receiver = MockReceiver()
        self.assertIsNone(receiver.received_sample)

        # Attach the receiver
        self.manager.attach_receiver(receiver)

        # No data at the beginning
        self.assertEqual(len(self.manager.buffer), 0)
        # Send the START signal
        self.manager.receive_signal(ControlSignal.START)
        # Still no data
        self.assertEqual(len(self.manager.buffer), 0)

        # Send some data
        self.manager.receive_data([1, 2, 3])
        self.manager.receive_data([4, 5, 6])
        self.manager.receive_data([7, 8, 9])

        # Check the data has been received
        self.assertEqual(len(self.manager.buffer), 3)

        # Send the STOP signal
        self.manager.receive_signal(ControlSignal.STOP)

        # Check if the Sample has been received correctly by the receiver
        self.assertIsNotNone(receiver.received_sample)
        # Check if the arrays are the same
        self.assertTrue(sp.allclose(receiver.received_sample.data, sp.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])))

    def test_sample_with_min_sample_length_should_fail(self):
        # Initialize a Mock Receiver
        receiver = MockReceiver()
        self.assertIsNone(receiver.received_sample)

        self.manager.min_sample_length = 10  # Set the minimum number of frames to 10

        # Attach the receiver
        self.manager.attach_receiver(receiver)

        # No data at the beginning
        self.assertEqual(len(self.manager.buffer), 0)
        # Send the START signal
        self.manager.receive_signal(ControlSignal.START)
        # Still no data
        self.assertEqual(len(self.manager.buffer), 0)

        # Send some data
        self.manager.receive_data([1, 2, 3])
        self.manager.receive_data([4, 5, 6])
        self.manager.receive_data([7, 8, 9])

        # Check the data has been received
        self.assertEqual(len(self.manager.buffer), 3)

        # Send the STOP signal
        self.manager.receive_signal(ControlSignal.STOP)

        # The sample doesn't have enough frames, so the receiver should not be notified
        self.assertIsNone(receiver.received_sample)

    def test_start_again_should_reset_buffer(self):
        # Initialize a Mock Receiver
        receiver = MockReceiver()
        self.assertIsNone(receiver.received_sample)

        # Attach the receiver
        self.manager.attach_receiver(receiver)

        # No data at the beginning
        self.assertEqual(len(self.manager.buffer), 0)
        # Send the START signal
        self.manager.receive_signal(ControlSignal.START)
        # Still no data
        self.assertEqual(len(self.manager.buffer), 0)

        # Send some data
        self.manager.receive_data([1, 2, 3])
        self.manager.receive_data([4, 5, 6])
        self.manager.receive_data([7, 8, 9])

        # Check the data has been received
        self.assertEqual(len(self.manager.buffer), 3)

        # Send the STOP signal
        self.manager.receive_signal(ControlSignal.STOP)

        # Check if the Sample has been received correctly by the receiver
        self.assertIsNotNone(receiver.received_sample)
        # Check if the arrays are the same
        self.assertTrue(sp.allclose(receiver.received_sample.data, sp.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])))

        # Start a new sample
        self.manager.receive_signal(ControlSignal.START)
        # No data
        self.assertEqual(len(self.manager.buffer), 0)


class StreamSampleManagerTestCase(unittest.TestCase):
    """
    Tests to check StreamSampleManager behaviour
    """
    def setUp(self):
        # Initialize the StreamSampleManager
        self.manager = StreamSampleManager(window=4, step=2)

    def tearDown(self):
        # Destroy the sample manager
        self.manager = None

    def test_sample_received_when_window_size_is_reached(self):
        # Initialize a Mock Receiver
        receiver = MockReceiver()
        self.assertIsNone(receiver.received_sample)

        # Attach the receiver
        self.manager.attach_receiver(receiver)

        # No data at the beginning
        self.assertEqual(len(self.manager.buffer), 0)
        # Send the START signal
        self.manager.receive_signal(ControlSignal.START)
        # Still no data
        self.assertEqual(len(self.manager.buffer), 0)

        # Send some data
        self.manager.receive_data([1, 2, 3])
        self.manager.receive_data([4, 5, 6])
        self.manager.receive_data([7, 8, 9])
        self.manager.receive_data([10, 11, 12])

        # Check if the Sample has been received correctly by the receiver
        self.assertIsNotNone(receiver.received_sample)
        # Check if the arrays are the same
        self.assertTrue(sp.allclose(receiver.received_sample.data,
                                    sp.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])))

    def test_step_working_correctly(self):
        # Initialize a Mock Receiver
        receiver = MockReceiver()
        self.assertIsNone(receiver.received_sample)

        # Attach the receiver
        self.manager.attach_receiver(receiver)

        # No data at the beginning
        self.assertEqual(len(self.manager.buffer), 0)
        # Send the START signal
        self.manager.receive_signal(ControlSignal.START)
        # Still no data
        self.assertEqual(len(self.manager.buffer), 0)

        # Send some data
        self.manager.receive_data([1, 2, 3])
        self.manager.receive_data([4, 5, 6])
        self.manager.receive_data([7, 8, 9])
        self.manager.receive_data([10, 11, 12])

        # Check if the Sample has been received correctly by the receiver
        self.assertIsNotNone(receiver.received_sample)
        # Check if the arrays are the same
        self.assertTrue(sp.allclose(receiver.received_sample.data,
                                    sp.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])))

        self.manager.receive_data([13, 14, 15])
        self.manager.receive_data([16, 17, 18])

        # Check the new sample data
        self.assertTrue(sp.allclose(receiver.received_sample.data,
                                    sp.array([[7, 8, 9], [10, 11, 12], [13, 14, 15], [16, 17, 18]])))

    def test_sample_stop_before_reaching_window_size(self):
        # Initialize a Mock Receiver
        receiver = MockReceiver()
        self.assertIsNone(receiver.received_sample)

        # Attach the receiver
        self.manager.attach_receiver(receiver)

        # No data at the beginning
        self.assertEqual(len(self.manager.buffer), 0)
        # Send the START signal
        self.manager.receive_signal(ControlSignal.START)
        # Still no data
        self.assertEqual(len(self.manager.buffer), 0)

        # Send some data
        self.manager.receive_data([1, 2, 3])
        self.manager.receive_data([4, 5, 6])
        self.manager.receive_data([7, 8, 9])

        # Check the data has been received
        self.assertEqual(len(self.manager.buffer), 3)

        # Send the STOP signal
        self.manager.receive_signal(ControlSignal.STOP)

        # Check if the Sample has been received correctly by the receiver
        self.assertIsNotNone(receiver.received_sample)
        # Check if the arrays are the same
        self.assertTrue(sp.allclose(receiver.received_sample.data, sp.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])))

    def test_step_must_be_lower_or_equal_to_window_size(self):
        # Check the StreamSampleManager raises an exception if step > window
        self.assertRaises(ValueError, StreamSampleManager, step=10, window=5)

if __name__ == '__main__':
    unittest.main()
