from pygarl.base import Sample
from .abstracts import ControlSignal, AbstractSampleManager


class DiscreteSampleManager(AbstractSampleManager):
    # TODO: Add min_sample_length, a parameter that filter samples too short, should be in self.package_sample()
    def __init__(self, axis=6):
        # Call the base constructor to initialize buffer and axis
        AbstractSampleManager.__init__(self, axis)

    def start_sample(self):
        """
        Called when a Start signal is received
        """
        # Empty the buffer
        self.buffer = []

    def end_sample(self):
        """
        Called when a Stop Signal is received, package the sample and notify the receivers
        """
        self.package_sample()

    def receive_signal(self, signal):
        """
        Called from a DataReader when a signal is received
        """
        # Call the appropriate method based on the received signal
        if signal == ControlSignal.START:
            # When a START signal is received, start a new sample
            self.start_sample()
        elif signal == ControlSignal.STOP:
            # When a STOP signal is received, end the sample
            self.end_sample()

    def receive_data(self, data):
        """
        Called from a DataReader when new data is available
        """
        # Add the current data frame to the buffer
        self.buffer.append(data)

    def package_sample(self):
        """
        Package the sample with the data in the buffer and notify all the attached receivers
        """
        # Create a sample with the buffer data
        sample = Sample(data=self.buffer)
        # Notify all the attached receivers
        self.notify_receivers(sample)


class StreamSampleManager(AbstractSampleManager):
    # TODO: Implementation and Tests
    def receive_signal(self, signal):
        pass

    def receive_data(self, data):
        pass

    def package_sample(self):
        pass
