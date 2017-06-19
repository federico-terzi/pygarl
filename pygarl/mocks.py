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
