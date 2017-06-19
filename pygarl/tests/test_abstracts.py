import unittest
from ..abstracts import *
from ..mocks import *

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


if __name__ == '__main__':
    unittest.main()
