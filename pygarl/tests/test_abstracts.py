import unittest
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


if __name__ == '__main__':
    unittest.main()
