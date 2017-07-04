from __future__ import print_function
from pygarl.abstracts import *


class MockSampleManager(AbstractSampleManager):
    """
    Mock implementation of the sample manager, used for tests
    """

    def __init__(self):
        AbstractSampleManager.__init__(self)

        self.received_data = None
        self.received_signal = None

    def receive_data(self, data):
        self.received_data = data

    def receive_signal(self, signal):
        self.received_signal = signal

    def package_sample(self):
        pass


class VerboseTestSampleManager(AbstractSampleManager):
    """
    Used to print the received values from a DataReader
    """

    def __init__(self):
        AbstractSampleManager.__init__(self)

    def receive_data(self, data):
        print("DATA:", data)

    def receive_signal(self, signal):
        print("SIGNAL:", signal)

    def package_sample(self):
        pass


class VerboseMiddleware(AbstractMiddleware):
    """
    Used to print the received sample
    """
    def __init__(self, verbose=True):
        AbstractMiddleware.__init__(self)
        self.counter = 0
        self.verbose = verbose

    def process_sample(self, sample):
        if self.verbose:
            print("SAMPLE "+str(self.counter))
            print(sample)
            self.counter += 1
        return sample


class MockReceiver(Receiver):
    """
    Mock implementation of the receiver, used for tests
    """
    def __init__(self):
        Receiver.__init__(self)

        self.received_sample = None

    def receive_sample(self, sample):
        self.received_sample = sample


class MockFunctionReceiver(object):
    """
    Used to test the callback manager
    """
    def __init__(self):
        self.received = False

    def receive(self):
        """
        When this function is called, self.received becomes true 
        """
        self.received = True


class MockCallbackManager(object):
    """
    Used to test the callback manager
    """
    def __init__(self):
        self.received_gesture = None

    def receive_gesture(self, gesture_id):
        """
        When this function is called, set self.received_gesture
        """
        self.received_gesture = gesture_id
