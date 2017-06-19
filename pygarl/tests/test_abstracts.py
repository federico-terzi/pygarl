import unittest
from ..abstracts import *
from ..mocks import *
from ..base import *

# To execute tests, go to the project main directory and type:
# python -m unittest discover


class AbstractDataReaderTestCase(unittest.TestCase):
    """
    Tests to check AbstractDataReader consistency
    """

    def setUp(self):
        # Initialize an AbstractDataReader
        self.abstract_data_reader = AbstractDataReader()

    def tearDown(self):
        # Destroy the AbstractDataReader
        self.abstract_data_reader = None

    def test_manager_attached_correctly(self):
        sample_manager = AbstractSampleManager()

        # Attach the manager
        self.abstract_data_reader.attach_manager(sample_manager)

        # Check if the manager is attached
        self.assertIn(sample_manager, self.abstract_data_reader.managers)

    def test_manager_detached_correctly(self):
        sample_manager = AbstractSampleManager()

        # Attach the manager
        self.abstract_data_reader.attach_manager(sample_manager)

        # Check if the manager is attached
        self.assertIn(sample_manager, self.abstract_data_reader.managers)

        # Detach the manager
        self.abstract_data_reader.detach_manager(sample_manager)

        # Check that the manager is not attached anymore
        self.assertNotIn(sample_manager, self.abstract_data_reader.managers)

    def test_notify_data(self):
        sample_manager = MockSampleManager()

        # Attach the manager
        self.abstract_data_reader.attach_manager(sample_manager)

        # Check that the received data is initially None
        self.assertIsNone(sample_manager.received_data)

        # Notify the data by sending True
        self.abstract_data_reader.notify_data(True)

        # Check that the received data is not none anymore
        self.assertIsNotNone(sample_manager.received_data)

        # Check that the received data is True
        self.assertTrue(sample_manager.received_data)

    def test_notify_signal(self):
        sample_manager = MockSampleManager()

        # Attach the manager
        self.abstract_data_reader.attach_manager(sample_manager)

        # Check that the received signal is initially None
        self.assertIsNone(sample_manager.received_signal)

        # Notify the signal by sending START
        self.abstract_data_reader.notify_signal(ControlSignal.START)

        # Check that the received signal is not none anymore
        self.assertIsNotNone(sample_manager.received_signal)

        # Check that the received data is START
        self.assertEqual(sample_manager.received_signal, ControlSignal.START)

    def test_mainloop_not_implemented(self):
        # The mainloop function must be abstract
        self.assertRaises(NotImplementedError, self.abstract_data_reader.mainloop)


class AbstractSampleManagerTestCase(unittest.TestCase):
    """
    Tests to check AbstractSampleManager consistency
    """

    def setUp(self):
        # Initialize an AbstractSampleManager
        self.abstract_sample_manager = AbstractSampleManager()

    def tearDown(self):
        # Destroy the AbstractSampleManager
        self.abstract_sample_manager = None

    def test_receiver_attached_correctly(self):
        receiver = Receiver()
        # Receiver must not be already attached
        self.assertNotIn(receiver, self.abstract_sample_manager.receivers)
        # Attach the receiver
        self.abstract_sample_manager.attach_receiver(receiver)
        # Check that the receiver is attached
        self.assertIn(receiver, self.abstract_sample_manager.receivers)

    def test_receiver_detached_correctly(self):
        receiver = Receiver()
        # Attach the receiver
        self.abstract_sample_manager.attach_receiver(receiver)
        # Check that the receiver is attached
        self.assertIn(receiver, self.abstract_sample_manager.receivers)
        # Detach the receiver
        self.abstract_sample_manager.detach_receiver(receiver)
        # Check that the receiver is detached
        self.assertNotIn(receiver, self.abstract_sample_manager.receivers)

    def test_notify_receivers(self):
        sample = Sample(None)
        receiver = MockReceiver()
        # Attach the receiver
        self.abstract_sample_manager.attach_receiver(receiver)
        # Initially the received sample must be none
        self.assertIsNone(receiver.received_sample)
        # Notify the receivers
        self.abstract_sample_manager.notify_receivers(sample)
        # The received sample must be equal to the sent one
        self.assertEqual(receiver.received_sample, sample)

    def test_receive_data_not_implemented(self):
        # The function must be abstract
        self.assertRaises(NotImplementedError, self.abstract_sample_manager.receive_data, None)

    def test_receive_signal_not_implemented(self):
        # The function must be abstract
        self.assertRaises(NotImplementedError, self.abstract_sample_manager.receive_signal, None)

    def test_package_sample_not_implemented(self):
        # The function must be abstract
        self.assertRaises(NotImplementedError, self.abstract_sample_manager.package_sample)

if __name__ == '__main__':
    unittest.main()
