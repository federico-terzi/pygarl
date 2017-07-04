import unittest
from pygarl.abstracts import *
from pygarl.mocks import *
from pygarl.base import *

# To execute tests, go to the project main directory and type:
# python -m unittest discover


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
