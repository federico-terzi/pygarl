import unittest

import shutil

from pygarl.abstracts import *
from pygarl.mocks import *
from pygarl.base import *

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


class SenderTestCase(unittest.TestCase):
    """
    Tests to check Sender consistency
    """
    def setUp(self):
        # Initialize a Sender
        self.sender = Sender()

    def tearDown(self):
        # Destroy the Sender
        self.sender = None

    def test_receiver_attached_correctly(self):
        receiver = Receiver()
        # Receiver must not be already attached
        self.assertNotIn(receiver, self.sender.receivers)
        # Attach the receiver
        self.sender.attach_receiver(receiver)
        # Check that the receiver is attached
        self.assertIn(receiver, self.sender.receivers)

    def test_receiver_detached_correctly(self):
        receiver = Receiver()
        # Attach the receiver
        self.sender.attach_receiver(receiver)
        # Check that the receiver is attached
        self.assertIn(receiver, self.sender.receivers)
        # Detach the receiver
        self.sender.detach_receiver(receiver)
        # Check that the receiver is detached
        self.assertNotIn(receiver, self.sender.receivers)

    def test_notify_receivers(self):
        sample = Sample([[]])
        receiver = MockReceiver()
        # Attach the receiver
        self.sender.attach_receiver(receiver)
        # Initially the received sample must be none
        self.assertIsNone(receiver.received_sample)
        # Notify the receivers
        self.sender.notify_receivers(sample)
        # The received sample must be equal to the sent one
        self.assertEqual(receiver.received_sample, sample)


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
        sample = Sample([[]])
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


class AbstractGesturePredictorTestCase(unittest.TestCase):
    """
    Tests to check AbstractGesturePredictor behaviour
    """

    def setUp(self):
        # Initialize an AbstractGesturePredictor
        self.abstract_gesture_predictor = AbstractGesturePredictor()

    def tearDown(self):
        # Destroy the AbstractGesturePredictor
        self.abstract_gesture_predictor = None

    def test_callback_manager_attached_correctly(self):
        callback_mg = CallbackManager()
        # Callback Manager must not be already attached
        self.assertNotIn(callback_mg, self.abstract_gesture_predictor.callbacks)
        # Attach the Callback Manager
        self.abstract_gesture_predictor.attach_callback_manager(callback_mg)
        # Check that the callback manager is attached
        self.assertIn(callback_mg, self.abstract_gesture_predictor.callbacks)

    def test_callback_manager_detached_correctly(self):
        callback_mg = CallbackManager()

        # Attach the Callback Manager
        self.abstract_gesture_predictor.attach_callback_manager(callback_mg)
        # Check that the callback manager is attached
        self.assertIn(callback_mg, self.abstract_gesture_predictor.callbacks)
        # Detach the Callback Manager
        self.abstract_gesture_predictor.detach_callback_manager(callback_mg)
        # Callback Manager must not be already attached
        self.assertNotIn(callback_mg, self.abstract_gesture_predictor.callbacks)

    def test_notify_callbacks(self):
        callback_mg = MockCallbackManager()

        self.abstract_gesture_predictor.attach_callback_manager(callback_mg)
        # Initially the received gesture is None
        self.assertIsNone(callback_mg.received_gesture)
        # Notify the gesture
        self.abstract_gesture_predictor.notify_callbacks("TEST")
        # Make sure the gesture has been received
        self.assertEqual(callback_mg.received_gesture, "TEST")

    def test_predict_not_implemented(self):
        sample = Sample([[]])
        # The function must be abstract
        self.assertRaises(NotImplementedError, self.abstract_gesture_predictor.predict, sample)


class AbstractMiddlewareTestCase(unittest.TestCase):
    """
    Tests to check AbstractMiddleware behaviour
    """

    def setUp(self):
        # Initialize an AbstractMiddleware
        self.abstract_middleware = AbstractMiddleware()

    def tearDown(self):
        # Destroy the AbstractMiddleware
        self.abstract_middleware = None

    def test_notify_receivers(self):
        sample = Sample([[]])
        receiver = MockReceiver()
        # Attach the receiver
        self.abstract_middleware.attach_receiver(receiver)
        # Initially the received sample must be none
        self.assertIsNone(receiver.received_sample)
        # Notify the receivers
        self.abstract_middleware.notify_receivers(sample)
        # The received sample must be equal to the sent one
        self.assertEqual(receiver.received_sample, sample)

    def test_receive_sample_and_notify_receivers(self):
        sample = Sample([[]])
        receiver = MockReceiver()
        # Attach the receiver
        self.abstract_middleware.attach_receiver(receiver)
        # Initially the received sample must be none
        self.assertIsNone(receiver.received_sample)
        # Send the sample to the receiver
        self.abstract_middleware.receive_sample(sample)
        # The received sample must be equal to the sent one
        self.assertEqual(receiver.received_sample, sample)

    def test_process_sample_should_not_process(self):
        sample = Sample([[]])
        # The function should return the sample without processing it ( in the abstract class )
        self.assertEqual(sample, self.abstract_middleware.process_sample(sample))


class AbstractClassifierTestCase(unittest.TestCase):
    """
    Tests to check AbstractClassifier consistency
    """

    def create_a_file(self, filename, content='{"gesture_id": "TESTSAMPLE", "data": [[1, 2, 3], [4, 5, 6]]}'):
        """
        Create a file, used for tests
        """
        with open(os.path.join("test_dir_abstract_classifier", filename), 'w') as output_file:
            output_file.write(content)

    def setUp(self):
        # Create a test directory if it doesn't exists
        if not os.path.exists("test_dir_abstract_classifier"):
            os.makedirs("test_dir_abstract_classifier")

        # Create a bunch of files
        self.create_a_file("id1_0_0.txt")
        self.create_a_file("id1_1_0.txt")
        self.create_a_file("id2_1_0.txt")
        self.create_a_file("id5_1_0.txt")
        self.create_a_file("id1_2_0.txt")

        # Initialize an AbstractClassifier
        self.classifier = AbstractClassifier(dataset_path="test_dir_abstract_classifier")

    def tearDown(self):
        # Destroy the test directory
        shutil.rmtree("test_dir_abstract_classifier")

        # Destroy the AbstractClassifier
        self.classifier = None

    def test_dataset_and_model_both_defined_should_raise_error(self):
        self.assertRaises(ValueError, AbstractClassifier, dataset_path="1", model_path="2")

    def test_at_least_one_dataset_or_model_must_be_defined_should_raise_error(self):
        self.assertRaises(ValueError, AbstractClassifier)

    def test_load_gestures_ids_should_fail_if_called_before_loading_samples_filenames(self):
        self.assertRaises(ValueError, self.classifier.load_gestures_ids)

    def test_load_gestures_ids_should_fail_if_dataset_path_is_not_defined(self):
        # Reset the dataset path
        self.classifier.dataset_path = None
        self.assertRaises(ValueError, self.classifier.load_gestures_ids)

    def test_load_samples_filenames_should_fail_if_dataset_path_is_not_defined(self):
        # Reset the dataset path
        self.classifier.dataset_path = None
        self.assertRaises(ValueError, self.classifier.load_samples_filenames)

    def test_load_samples_filenames(self):
        filenames = self.classifier.load_samples_filenames()

        self.assertIn("id1_0_0.txt", filenames)
        self.assertIn("id1_1_0.txt", filenames)
        self.assertIn("id2_1_0.txt", filenames)
        self.assertIn("id5_1_0.txt", filenames)
        self.assertIn("id1_2_0.txt", filenames)

    def test_load_gestures_ids(self):
        self.classifier.load_samples_filenames()

        ids = self.classifier.load_gestures_ids()

        self.assertIn("id1", ids)
        self.assertIn("id2", ids)
        self.assertIn("id5", ids)

    def test_get_gesture_id_from_filename(self):
        self.assertEqual("id1", AbstractClassifier.get_gesture_id_from_filename("id1_0_0"))

    def test_load_samples_data_should_fail_if_called_before_loading_samples_filenames(self):
        self.assertRaises(ValueError, self.classifier.load_samples_data)

    def test_load_samples_data_should_fail_if_dataset_path_is_not_defined(self):
        # Reset the dataset path
        self.classifier.dataset_path = None
        self.assertRaises(ValueError, self.classifier.load_samples_data)

    def test_load_samples_data(self):
        # Substitute the load_sample_data method of the classifier with a Mock
        mock = MockFunctionCounter()

        self.classifier.load_sample_data = mock.callback
        # Counter must be zero initially
        self.assertEqual(mock.counter, 0)

        self.classifier.load_samples_filenames()
        self.classifier.load_samples_data()

        # Counter must be zero initially
        self.assertEqual(mock.counter, len(self.classifier.samples_filenames))

    def test_predict_should_fail_if_the_model_is_not_trained(self):
        self.assertFalse(self.classifier.is_trained)

        self.assertRaises(ValueError, self.classifier.predict, Sample([[]]))

    def test_plot_confusion_matrix_should_fail_before_training(self):
        self.assertRaises(ValueError, self.classifier.plot_confusion_matrix)


if __name__ == '__main__':
    unittest.main()
