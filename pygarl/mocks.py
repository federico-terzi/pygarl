from .abstracts import *


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
